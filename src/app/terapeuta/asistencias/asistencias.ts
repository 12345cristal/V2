import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { TerapeutaService, AsistenciaDTO, ReprogramacionDTO } from '../../service/terapeuta.service';

export interface SesionAsistencia {
  id_sesion: number;
  id_nino: number;
  nombre_nino: string;
  fotografia?: string;
  terapia: string;
  fecha: Date;
  hora_inicio: string;
  hora_fin: string;
  sala: string;
  estado_asistencia: 'pendiente' | 'asistio' | 'cancelada' | 'reprogramada';
  asistencia_registrada: boolean;
  fecha_registro?: Date;
  nota_asistencia?: string;
  puede_editar: boolean;
}

@Component({
  selector: 'app-asistencias-terapeuta',
  standalone: true,
  imports: [CommonModule, FormsModule, MatIconModule],
  templateUrl: './asistencias.html',
  styleUrls: ['./asistencias-mejorado.scss']
})
export class AsistenciasTerapeutaComponent implements OnInit {
  
  sesiones = signal<SesionAsistencia[]>([]);
  cargando = signal<boolean>(false);
  
  periodoSeleccionado = 'hoy';
  estadoFiltro = 'todos';
  busquedaNino = '';

  mostrarModalReprogramacion = signal<boolean>(false);
  sesionReprogramar = signal<SesionAsistencia | null>(null);
  nuevaFechaReprogramacion = '';
  nuevaHoraReprogramacion = '';
  motivoReprogramacion = '';

  sesionesFiltradas = computed(() => {
    let sesiones = this.sesiones();

    // Filtrar por estado
    if (this.estadoFiltro !== 'todos') {
      sesiones = sesiones.filter(s => s.estado_asistencia === this.estadoFiltro);
    }

    // Filtrar por búsqueda
    if (this.busquedaNino.trim()) {
      const busqueda = this.busquedaNino.toLowerCase();
      sesiones = sesiones.filter(s => 
        s.nombre_nino.toLowerCase().includes(busqueda)
      );
    }

    return sesiones;
  });

  constructor(
    private router: Router,
    private terapeutaService: TerapeutaService
  ) {}

  ngOnInit(): void {
    this.cargarAsistencias();
  }

  cargarAsistencias(): void {
    this.cargando.set(true);
    
    this.terapeutaService.obtenerAsistencias(this.periodoSeleccionado).subscribe({
      next: (sesiones) => {
        this.sesiones.set(sesiones);
        this.cargando.set(false);
      },
      error: (error) => {
        console.error('Error al cargar asistencias:', error);
        this.cargando.set(false);
        alert('Error al cargar las asistencias');
      }
    });
  }

  filtrar(): void {
    // La computación se hace automáticamente
    console.log('Filtrando...');
  }

  tieneAsistenciasPendientes(): boolean {
    return this.sesiones().some(s => !s.asistencia_registrada);
  }

  contarPendientes(): number {
    return this.sesiones().filter(s => !s.asistencia_registrada).length;
  }

  filtrarPendientes(): void {
    this.estadoFiltro = 'pendiente';
    this.filtrar();
  }

  registrarAsistencia(idSesion: number, estado: 'asistio' | 'cancelada'): void {
    const asistenciaDTO: AsistenciaDTO = {
      id_sesion: idSesion,
      estado: estado,
      fecha_registro: new Date().toISOString()
    };

    this.terapeutaService.registrarAsistencia(asistenciaDTO).subscribe({
      next: (response) => {
        console.log('Asistencia registrada:', response);
        
        // Actualizar localmente
        const sesionesActualizadas = this.sesiones().map(s => {
          if (s.id_sesion === idSesion) {
            return {
              ...s,
              estado_asistencia: estado,
              asistencia_registrada: true,
              fecha_registro: new Date()
            };
          }
          return s;
        });

        this.sesiones.set(sesionesActualizadas);
        alert(`Asistencia registrada como: ${estado === 'asistio' ? 'Asistió' : 'Cancelada'}`);
      },
      error: (error) => {
        console.error('Error al registrar asistencia:', error);
        alert(`Error al registrar la asistencia: ${error.message}`);
      }
    });
  }

  abrirReprogramacion(sesion: SesionAsistencia): void {
    this.sesionReprogramar.set(sesion);
    this.mostrarModalReprogramacion.set(true);
  }

  cerrarModalReprogramacion(): void {
    this.mostrarModalReprogramacion.set(false);
    this.sesionReprogramar.set(null);
    this.nuevaFechaReprogramacion = '';
    this.nuevaHoraReprogramacion = '';
    this.motivoReprogramacion = '';
  }

  confirmarReprogramacion(): void {
    if (!this.nuevaFechaReprogramacion || !this.nuevaHoraReprogramacion) {
      alert('Por favor completa la fecha y hora');
      return;
    }

    const sesion = this.sesionReprogramar();
    if (!sesion) return;

    const reprogramacionDTO: ReprogramacionDTO = {
      id_sesion: sesion.id_sesion,
      nueva_fecha: this.nuevaFechaReprogramacion,
      nueva_hora: this.nuevaHoraReprogramacion,
      motivo: this.motivoReprogramacion
    };

    this.terapeutaService.reprogramarSesion(reprogramacionDTO).subscribe({
      next: (response) => {
        console.log('Sesión reprogramada:', response);
        alert('Sesión reprogramada exitosamente');
        this.cerrarModalReprogramacion();
        this.cargarAsistencias();
      },
      error: (error) => {
        console.error('Error al reprogramar sesión:', error);
        alert(`Error al reprogramar: ${error.message}`);
      }
    });
  }

  editarAsistencia(sesion: SesionAsistencia): void {
    console.log('Editar asistencia:', sesion);
    // Implementar lógica de edición
  }

  exportarAsistencias(): void {
    console.log('Exportando asistencias...');
    // Implementar lógica de exportación
    alert('Función de exportación en desarrollo');
  }

  getEstadoClase(estado: string): string {
    const clases: any = {
      'pendiente': 'estado-pendiente',
      'asistio': 'estado-asistio',
      'cancelada': 'estado-cancelada',
      'reprogramada': 'estado-reprogramada'
    };
    return clases[estado] || '';
  }

  getEstadoTexto(estado: string): string {
    const textos: any = {
      'pendiente': 'Pendiente',
      'asistio': 'Asistió',
      'cancelada': 'Cancelada',
      'reprogramada': 'Reprogramada'
    };
    return textos[estado] || 'Desconocido';
  }

  volver(): void {
    this.router.navigate(['/terapeuta/inicio']);
  }
}



