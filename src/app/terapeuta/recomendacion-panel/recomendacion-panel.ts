// src/app/terapeuta/recomendacion-panel/recomendacion-panel.ts
import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecomendacionService } from '../../service/recomendacion.service';
import { TerapeutaPacientesService } from '../../service/terapeuta-pacientes.service';
import { 
  RecomendacionActividad, 
  RecomendacionTerapia 
} from '../../interfaces/recomendacion.interface';

interface NinoConRecomendaciones {
  id: number;
  nombre_completo: string;
  actividades: RecomendacionActividad[];
  terapias: RecomendacionTerapia[];
  expandido: boolean;
}

/**
 * Componente para mostrar recomendaciones de actividades para los pacientes del terapeuta
 * Solo accesible para rol TERAPEUTA
 */
@Component({
  selector: 'app-recomendacion-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './recomendacion-panel.html',
  styleUrls: ['./recomendacion-panel.scss']
})
export class RecomendacionPanelTerapeutaComponent implements OnInit {
  // Signals para estado reactivo
  ninos = signal<NinoConRecomendaciones[]>([]);
  cargando = signal<boolean>(false);
  mensajeError = signal<string>('');
  
  // Configuración
  topN = 5; // Mostrar top 5 recomendaciones por niño

  constructor(
    private recomendacionService: RecomendacionService,
    private pacientesService: TerapeutaPacientesService
  ) {}

  ngOnInit(): void {
    this.cargarPacientesConRecomendaciones();
  }

  /**
   * Carga los pacientes del terapeuta y sus recomendaciones
   */
  async cargarPacientesConRecomendaciones(): Promise<void> {
    this.cargando.set(true);
    this.mensajeError.set('');

    try {
      // Obtener pacientes del terapeuta
      const pacientes: any = await this.pacientesService.getPacientesAsignados().toPromise();
      
      if (!pacientes || pacientes.length === 0) {
        this.cargando.set(false);
        return;
      }

      // Cargar recomendaciones para cada paciente
      const ninosConRecomendaciones: NinoConRecomendaciones[] = [];

      for (const paciente of pacientes) {
        try {
          const [actividades, terapias] = await Promise.all([
            this.recomendacionService.getRecomendacionActividades(paciente.id, this.topN).toPromise(),
            this.recomendacionService.getRecomendacionTerapias(paciente.id, this.topN).toPromise()
          ]);

          ninosConRecomendaciones.push({
            id: paciente.id,
            nombre_completo: `${paciente.nombre} ${paciente.apellido_paterno}`,
            actividades: actividades || [],
            terapias: terapias || [],
            expandido: false
          });
        } catch (error: any) {
          console.error(`Error al cargar recomendaciones para niño ${paciente.id}:`, error);
          // Continuar con los demás pacientes
        }
      }

      this.ninos.set(ninosConRecomendaciones);
      this.cargando.set(false);
    } catch (error: any) {
      this.mensajeError.set('Error al cargar pacientes: ' + error.message);
      this.cargando.set(false);
    }
  }

  /**
   * Alterna la expansión de las recomendaciones de un niño
   */
  toggleExpandir(ninoId: number): void {
    this.ninos.update(ninos => 
      ninos.map(n => 
        n.id === ninoId 
          ? { ...n, expandido: !n.expandido } 
          : n
      )
    );
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
   * Obtiene la clase CSS para el score badge
   */
  getScoreClass(score: number): string {
    if (score >= 0.7) return 'score-high';
    if (score >= 0.4) return 'score-medium';
    return 'score-low';
  }
}



