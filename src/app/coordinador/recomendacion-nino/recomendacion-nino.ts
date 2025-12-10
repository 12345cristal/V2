// src/app/coordinador/recomendacion-nino/recomendacion-nino.ts
import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RecomendacionService } from '../../service/recomendacion.service';
import { NinosService } from '../../service/ninos.service';
import { 
  RecomendacionActividad, 
  RecomendacionTerapia 
} from '../../interfaces/recomendacion.interface';

/**
 * Componente para visualizar recomendaciones de actividades y terapias por niño
 * Solo accesible para rol COORDINADOR
 */
@Component({
  selector: 'app-recomendacion-nino',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './recomendacion-nino.html',
  styleUrls: ['./recomendacion-nino.scss']
})
export class RecomendacionNinoComponent implements OnInit {
  // Signals para estado reactivo
  ninos = signal<any[]>([]);
  ninoSeleccionado = signal<number | null>(null);
  recomendacionesActividades = signal<RecomendacionActividad[]>([]);
  recomendacionesTerapias = signal<RecomendacionTerapia[]>([]);
  cargando = signal<boolean>(false);
  cargandoNinos = signal<boolean>(false);
  mensajeError = signal<string>('');
  mensajeExito = signal<string>('');
  mensajeAdvertencia = signal<string>('');
  
  // Configuración
  topN = 10;

  constructor(
    private recomendacionService: RecomendacionService,
    private ninosService: NinosService
  ) {}

  ngOnInit(): void {
    this.cargarNinos();
  }

  /**
   * Carga la lista de niños activos
   */
  cargarNinos(): void {
    this.cargandoNinos.set(true);
    this.mensajeError.set('');
    
    this.ninosService.getNinos().subscribe({
      next: (data: any[]) => {
        const ninosActivos = data.filter((n: any) => n.estado === 'ACTIVO');
        this.ninos.set(ninosActivos);
        this.cargandoNinos.set(false);
        
        if (ninosActivos.length === 0) {
          this.mensajeAdvertencia.set('⚠️ No hay niños activos registrados en el sistema.');
        }
      },
      error: (error: any) => {
        const mensaje = error.error?.detail || error.message || 'Error desconocido';
        this.mensajeError.set(`❌ Error al cargar niños: ${mensaje}`);
        this.cargandoNinos.set(false);
      }
    });
  }

  /**
   * Cuando el usuario selecciona un niño
   */
  onNinoSeleccionado(event: any): void {
    const ninoId = parseInt(event.target.value);
    if (ninoId) {
      this.ninoSeleccionado.set(ninoId);
      this.cargarRecomendaciones(ninoId);
    } else {
      this.ninoSeleccionado.set(null);
      this.recomendacionesActividades.set([]);
      this.recomendacionesTerapias.set([]);
    }
  }

  /**
   * Carga las recomendaciones para el niño seleccionado
   */
  cargarRecomendaciones(ninoId: number): void {
    this.cargando.set(true);
    this.mensajeError.set('');
    this.mensajeExito.set('');
    this.mensajeAdvertencia.set('');
    this.recomendacionesActividades.set([]);
    this.recomendacionesTerapias.set([]);

    // Cargar actividades y terapias en paralelo
    Promise.all([
      this.recomendacionService.getRecomendacionActividades(ninoId, this.topN).toPromise(),
      this.recomendacionService.getRecomendacionTerapias(ninoId, this.topN).toPromise()
    ]).then(([actividades, terapias]) => {
      this.recomendacionesActividades.set(actividades || []);
      this.recomendacionesTerapias.set(terapias || []);
      this.cargando.set(false);
      
      const totalRecomendaciones = (actividades?.length || 0) + (terapias?.length || 0);
      
      if (totalRecomendaciones === 0) {
        this.mensajeAdvertencia.set('⚠️ No se encontraron recomendaciones para este niño. Asegúrese de que el niño tenga un perfil completo y que existan actividades/terapias registradas.');
      } else {
        this.mensajeExito.set(`✅ Se encontraron ${actividades?.length || 0} actividades y ${terapias?.length || 0} terapias recomendadas.`);
        setTimeout(() => this.mensajeExito.set(''), 4000);
      }
    }).catch((error: any) => {
      const mensaje = error.error?.detail || error.message || 'Error desconocido al obtener recomendaciones';
      this.mensajeError.set(`❌ Error al cargar recomendaciones: ${mensaje}`);
      this.cargando.set(false);
      console.error('Error recomendaciones:', error);
    });
  }

  /**
   * Obtiene el color de la barra de progreso según el score
   */
  getScoreColor(score: number): string {
    if (score >= 0.7) return '#28a745'; // Verde
    if (score >= 0.4) return '#ffc107'; // Amarillo
    return '#dc3545'; // Rojo
  }

  /**
   * Obtiene el nombre completo del niño seleccionado
   */
  getNombreNinoSeleccionado(): string {
    if (!this.ninoSeleccionado()) return '';
    const nino = this.ninos().find(n => n.id === this.ninoSeleccionado());
    return nino ? `${nino.nombre} ${nino.apellido_paterno}` : '';
  }
}
