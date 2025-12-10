import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { TopsisService } from '../../service/topsis.service';
import { TherapyService } from '../../service/terapias.service';
import { 
  PesosCriterios, 
  TopsisEvaluacionRequest, 
  TopsisResultado, 
  TerapeutaRanking 
} from '../../interfaces/topsis-terapeutas.interface';
import { Terapia } from '../../interfaces/terapia.interfaz';

@Component({
  selector: 'app-topsis-terapeutas',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './topsis-terapeutas.html',
  styleUrls: ['./topsis-terapeutas.scss']
})
export class TopsisTerapeutasComponent implements OnInit {

  // Pesos configurables para cada criterio
  pesos: PesosCriterios = {
    carga_laboral: 0.30,
    sesiones_completadas: 0.25,
    rating: 0.30,
    especialidad: 0.15
  };

  // Terapia específica (opcional)
  terapiaId: number | null = null;
  incluirInactivos = false;

  // Lista de terapias disponibles
  terapiasDisponibles: Terapia[] = [];

  // Resultado de la evaluación
  resultado: TopsisResultado | null = null;
  
  // Estados de la UI
  mensajeError: string | null = '';
  mensajeInfo: string | null = '';
  cargando = false;
  mostrarConfiguracion = true;

  constructor(
    private topsisSrv: TopsisService,
    private terapiasSrv: TherapyService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.cargarDatosIniciales();
  }

  /**
   * Carga datos iniciales: pesos default y terapias disponibles
   */
  cargarDatosIniciales(): void {
    this.cargando = true;
    this.mensajeInfo = 'Cargando datos...';

    // Cargar solo las terapias (pesos ya están por defecto)
    this.terapiasSrv.getTerapias().subscribe({
      next: (terapias) => {
        // Cargar terapias activas
        this.terapiasDisponibles = terapias.filter(t => t.estado === 'ACTIVA');
        
        this.cargando = false;
        this.mensajeInfo = `✓ Sistema listo. ${this.terapiasDisponibles.length} terapias disponibles. Ajusta los pesos y calcula.`;
        console.log('✅ Terapias cargadas:', this.terapiasDisponibles);
      },
      error: (err) => {
        console.error('❌ Error al cargar terapias:', err);
        this.cargando = false;
        this.mensajeError = 'Error al cargar las terapias. Verifica la conexión con el servidor.';
      }
    });
  }

  /**
   * Valida que la suma de pesos sea exactamente 1.0
   */
  validarPesos(): boolean {
    const suma = this.pesos.carga_laboral + this.pesos.sesiones_completadas + 
                 this.pesos.rating + this.pesos.especialidad;
    const diferencia = Math.abs(suma - 1.0);
    return diferencia < 0.01;
  }

  /**
   * Obtiene la suma actual de los pesos
   */
  getSumaPesos(): number {
    return this.pesos.carga_laboral + this.pesos.sesiones_completadas + 
           this.pesos.rating + this.pesos.especialidad;
  }

  /**
   * Normaliza los pesos proporcionalmente para que sumen 1.0
   */
  normalizarPesos(): void {
    const suma = this.getSumaPesos();
    if (suma > 0) {
      this.pesos.carga_laboral /= suma;
      this.pesos.sesiones_completadas /= suma;
      this.pesos.rating /= suma;
      this.pesos.especialidad /= suma;
      this.mensajeInfo = '✓ Pesos normalizados correctamente';
    }
  }

  /**
   * Calcula la evaluación TOPSIS con los pesos configurados
   */
  calcular(): void {
    // Validar pesos
    if (!this.validarPesos()) {
      this.mensajeError = `⚠️ Los pesos deben sumar 1.0. Actualmente suman ${this.getSumaPesos().toFixed(3)}. Usa "Normalizar" para corregir.`;
      return;
    }

    // Construir request
    const request: TopsisEvaluacionRequest = {
      pesos: this.pesos,
      incluir_inactivos: this.incluirInactivos
    };

    // Agregar terapia_id si se especificó (convertir a número si viene como string)
    if (this.terapiaId && Number(this.terapiaId) > 0) {
      request.terapia_id = Number(this.terapiaId);
    }

    // Debug: mostrar lo que se va a enviar
    console.log('🚀 Request a enviar:', JSON.stringify(request, null, 2));
    console.log('📊 Pesos:', request.pesos);

    // Limpiar mensajes y estados
    this.mensajeError = '';
    this.mensajeInfo = '';
    this.cargando = true;
    this.resultado = null;
    
    // Llamar al nuevo endpoint profesional
    this.topsisSrv.evaluarTerapeutasProfesional(request).subscribe({
      next: (res: TopsisResultado) => {
        console.log('✅ Evaluación TOPSIS completada:', res);
        console.log('📊 Ranking recibido:', res.ranking);
        console.log('📊 Total evaluados:', res.total_evaluados);
        
        this.resultado = res;
        this.cargando = false;
        this.mostrarConfiguracion = false;
        
        if (res.total_evaluados === 0) {
          this.mensajeInfo = '⚠️ No se encontraron terapeutas para evaluar con los criterios especificados.';
        } else {
          this.mensajeInfo = `✓ Evaluación completada: ${res.total_evaluados} terapeuta(s) evaluado(s)`;
        }
        
        // Forzar detección de cambios
        this.cdr.detectChanges();
        
        // Scroll a resultados después de que Angular actualice la vista
        setTimeout(() => {
          const resultSection = document.querySelector('.results-section');
          if (resultSection) {
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
          } else {
            console.warn('⚠️ No se encontró la sección de resultados');
          }
        }, 100);
      },
      error: (err) => {
        console.error('❌ Error al calcular TOPSIS:', err);
        console.error('📋 Error detail:', err.error);
        console.error('📋 Error message:', err.message);
        console.error('📋 Error status:', err.status);
        
        // Mostrar error detallado
        let errorMsg = 'Error al evaluar terapeutas.';
        if (err.error?.detail) {
          errorMsg = typeof err.error.detail === 'string' 
            ? err.error.detail 
            : JSON.stringify(err.error.detail);
        } else if (err.error?.errores) {
          errorMsg = err.error.errores.map((e: any) => `${e.campo}: ${e.mensaje}`).join('; ');
        }
        
        this.mensajeError = errorMsg;
        this.cargando = false;
      }
    });
  }

  /**
   * Reinicia el formulario para una nueva evaluación
   */
  nuevaEvaluacion(): void {
    this.resultado = null;
    this.mostrarConfiguracion = true;
    this.mensajeError = '';
    this.mensajeInfo = '✓ Ajusta los pesos y calcula una nueva evaluación.';
  }

  /**
   * Obtiene color según el ranking
   */
  getRankingBadgeClass(ranking: number): string {
    if (ranking === 1) return 'badge-gold';
    if (ranking === 2) return 'badge-silver';
    if (ranking === 3) return 'badge-bronze';
    return 'badge-default';
  }

  /**
   * Obtiene color del score
   */
  getScoreColor(score: number): string {
    if (score >= 0.75) return '#10b981'; // verde
    if (score >= 0.50) return '#3b82f6'; // azul
    if (score >= 0.25) return '#f59e0b'; // naranja
    return '#ef4444'; // rojo
  }

  /**
   * Formatea número a 2 decimales
   */
  formatNumber(num: number): string {
    return num.toFixed(2);
  }
}
