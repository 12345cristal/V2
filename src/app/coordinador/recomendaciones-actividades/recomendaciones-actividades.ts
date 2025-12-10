// src/app/coordinador/recomendaciones-actividades/recomendaciones-actividades.ts
import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import {
  RecomendacionesActividadesService,
  RecomendacionResponse,
  ActividadRecomendada,
  RecomendacionRequest,
  PerfilNino
} from '../../service/recomendaciones-actividades.service';
import { NinosService } from '../../service/ninos.service';
import { Nino } from '../../interfaces/nino.interface';

@Component({
  selector: 'app-recomendaciones-actividades',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './recomendaciones-actividades.html',
  styleUrls: ['./recomendaciones-actividades.scss']
})
export class RecomendacionesActividadesComponent implements OnInit {
  // Datos
  ninos: Nino[] = [];
  ninoSeleccionado: number | null = null;
  perfilNino: PerfilNino | null = null;
  recomendaciones: ActividadRecomendada[] = [];
  
  // Configuración
  topN: number = 10;
  filtrarArea: string = '';
  nivelDificultadMax: string = '';
  
  // Estados
  cargando: boolean = false;
  cargandoPerfil: boolean = false;
  error: string | null = null;
  mensaje: string | null = null;
  
  // Modal de detalles
  actividadDetalle: ActividadRecomendada | null = null;
  mostrarModalDetalle: boolean = false;
  mostrarModalAsignar: boolean = false;
  
  // Actividades asignadas
  actividadesAsignadas: Array<{
    actividad_id: number;
    nombre: string;
    descripcion: string | null;
    area_desarrollo: string | null;
    dificultad: number;
    duracion_minutos: number;
    score: number;
    ranking: number;
    razon: string;
    fecha_asignacion: string;
  }> = [];
  
  // Filtros
  areasDesarrollo = [
    { value: null, label: 'Todas las áreas' },
    { value: 'cognitivo', label: 'Cognitivo' },
    { value: 'motor', label: 'Motor' },
    { value: 'lenguaje', label: 'Lenguaje' },
    { value: 'social', label: 'Social' },
    { value: 'emocional', label: 'Emocional' }
  ];
  
  nivelesDificultad = [
    { value: null, label: 'Todas las dificultades' },
    { value: 1, label: 'Solo Baja' },
    { value: 2, label: 'Hasta Media' },
    { value: 3, label: 'Todas (incluye Alta)' }
  ];

  // Variables para navegación
  ninoIdDesdeRuta: number | null = null;
  nombreNinoVolver: string = '';
  mostrarBotonVolver: boolean = false;

  constructor(
    private recomendacionesService: RecomendacionesActividadesService,
    private ninosService: NinosService,
    private cdr: ChangeDetectorRef,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit() {
    this.cargarNinos();
    
    // Verificar si viene un ninoId desde la ruta (desde perfil)
    this.route.queryParams.subscribe(params => {
      if (params['ninoId']) {
        this.ninoIdDesdeRuta = +params['ninoId'];
        console.log('🔗 Navegación desde perfil - Niño ID:', this.ninoIdDesdeRuta);
        this.mostrarBotonVolver = true;
      }
    });
  }

  cargarNinos() {
    this.ninosService.getNinos().subscribe({
      next: (ninos: Nino[]) => {
        this.ninos = ninos;
        console.log('✅ Niños cargados:', this.ninos.length);
        
        // Si venimos desde perfil, pre-seleccionar el niño
        if (this.ninoIdDesdeRuta) {
          this.ninoSeleccionado = this.ninoIdDesdeRuta;
          
          // Obtener nombre del niño para el botón volver
          const nino = this.ninos.find(n => n.id === this.ninoIdDesdeRuta);
          if (nino) {
            this.nombreNinoVolver = `${nino.nombre} ${nino.apellidoPaterno} ${nino.apellidoMaterno}`;
            console.log('✅ Niño pre-seleccionado:', this.nombreNinoVolver);
            
            // Cargar perfil automáticamente
            this.onNinoChange();
          }
        }
      },
      error: (err: any) => {
        console.error('❌ Error cargando niños:', err);
        this.error = 'Error al cargar la lista de niños';
      }
    });
  }
  
  volverAPerfil() {
    if (this.ninoIdDesdeRuta) {
      this.router.navigate(['/coordinador/nino', this.ninoIdDesdeRuta, 'perfil']);
    }
  }

  onNinoChange() {
    if (this.ninoSeleccionado) {
      this.cargarPerfilNino();
      this.recomendaciones = [];
    } else {
      this.perfilNino = null;
      this.recomendaciones = [];
    }
  }

  cargarPerfilNino() {
    if (!this.ninoSeleccionado) return;
    
    this.cargandoPerfil = true;
    this.error = null;
    
    this.recomendacionesService.obtenerPerfilNino(this.ninoSeleccionado).subscribe({
      next: (perfil) => {
        this.perfilNino = perfil;
        this.cargandoPerfil = false;
        this.cdr.detectChanges();
        
        if (!perfil.tiene_embedding) {
          this.mensaje = 'Este niño aún no tiene perfil vectorizado. Genera recomendaciones para crearlo.';
        }
      },
      error: (err) => {
        console.error('❌ Error cargando perfil:', err);
        this.error = 'Error al cargar el perfil del niño';
        this.cargandoPerfil = false;
        this.cdr.detectChanges();
      }
    });
  }

  generarRecomendaciones() {
    if (!this.ninoSeleccionado) {
      this.error = 'Por favor selecciona un niño';
      return;
    }
    
    this.cargando = true;
    this.error = null;
    this.mensaje = null;
    
    const request: RecomendacionRequest = {
      nino_id: this.ninoSeleccionado,
      top_n: this.topN,
      filtrar_por_area: this.filtrarArea || null,
      nivel_dificultad_max: this.nivelDificultadMax ? parseInt(this.nivelDificultadMax) : null
    };
    
    console.log('🚀 Generando recomendaciones:', request);
    
    this.recomendacionesService.generarRecomendaciones(request).subscribe({
      next: (response) => {
        console.log('✅ Recomendaciones recibidas:', response);
        this.recomendaciones = response.recomendaciones;
        this.mensaje = `Se generaron ${response.total_recomendaciones} recomendaciones`;
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('❌ Error generando recomendaciones:', err);
        this.error = err.error?.detail || 'Error al generar recomendaciones';
        this.cargando = false;
        this.cdr.detectChanges();
      }
    });
  }

  obtenerColorScore(score: number): string {
    if (score >= 0.8) return '#22c55e'; // Verde
    if (score >= 0.6) return '#3b82f6'; // Azul
    if (score >= 0.4) return '#f59e0b'; // Naranja
    return '#ef4444'; // Rojo
  }

  obtenerIconoDificultad(dificultad: number): string {
    switch(dificultad) {
      case 1: return '⭐';
      case 2: return '⭐⭐';
      case 3: return '⭐⭐⭐';
      default: return '⭐';
    }
  }

  obtenerTextoDificultad(dificultad: number): string {
    switch(dificultad) {
      case 1: return 'Baja';
      case 2: return 'Media';
      case 3: return 'Alta';
      default: return 'Desconocida';
    }
  }

  limpiarResultados() {
    this.recomendaciones = [];
    this.mensaje = null;
    this.error = null;
  }

  resetearFiltros() {
    this.filtrarArea = '';
    this.nivelDificultadMax = '';
    this.topN = 10;
  }

  estaAsignada(actividadId: number): boolean {
    return this.actividadesAsignadas.some(a => a.actividad_id === actividadId);
  }

  onTopNChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    const value = parseInt(input.value);
    if (!isNaN(value) && value >= 1 && value <= 50) {
      this.topN = value;
      console.log('📊 Top N cambiado a:', this.topN);
    }
  }

  onAreaChange(event: Event): void {
    const select = event.target as HTMLSelectElement;
    this.filtrarArea = select.value;
    console.log('🎨 Área seleccionada:', this.filtrarArea || 'Todas');
  }

  onDificultadChange(event: Event): void {
    const select = event.target as HTMLSelectElement;
    this.nivelDificultadMax = select.value;
    console.log('⭐ Dificultad seleccionada:', this.nivelDificultadMax || 'Todas');
  }

  verDetalles(actividad: ActividadRecomendada) {
    this.actividadDetalle = actividad;
    this.mostrarModalDetalle = true;
  }

  cerrarModalDetalle() {
    this.mostrarModalDetalle = false;
    // Limpiar actividadDetalle después de cerrar la animación
    setTimeout(() => {
      this.actividadDetalle = null;
    }, 300);
  }

  abrirModalAsignar(actividad: ActividadRecomendada) {
    console.log('📦 Abriendo modal de asignación:', actividad.nombre);
    this.actividadDetalle = actividad;
    this.mostrarModalAsignar = true;
    this.cdr.detectChanges();
    console.log('✅ Modal de asignación abierto:', this.mostrarModalAsignar);
  }

  cerrarModalAsignar() {
    this.mostrarModalAsignar = false;
    // Limpiar actividadDetalle después de cerrar la animación
    setTimeout(() => {
      this.actividadDetalle = null;
    }, 300);
  }

  asignarActividad() {
    console.log('🎯 Intentando asignar actividad...');
    
    if (!this.actividadDetalle) {
      console.error('❌ No hay actividad seleccionada');
      this.error = 'No hay actividad seleccionada';
      return;
    }
    
    if (!this.ninoSeleccionado) {
      console.error('❌ No hay niño seleccionado');
      this.error = 'No hay niño seleccionado';
      return;
    }
    
    // Guardar datos completos antes de cerrar el modal
    const actividadCompleta = {
      actividad_id: this.actividadDetalle.actividad_id,
      nombre: this.actividadDetalle.nombre,
      descripcion: this.actividadDetalle.descripcion,
      area_desarrollo: this.actividadDetalle.area_desarrollo,
      dificultad: this.actividadDetalle.dificultad,
      duracion_minutos: this.actividadDetalle.duracion_minutos,
      score: this.actividadDetalle.score_similitud,
      ranking: this.actividadDetalle.ranking,
      razon: this.actividadDetalle.razon_recomendacion,
      fecha_asignacion: new Date().toISOString()
    };
    
    const ninoNombre = this.perfilNino?.nombre_nino || 'el niño';
    
    console.log('✅ Asignando actividad:', {
      actividad_id: actividadCompleta.actividad_id,
      actividad_nombre: actividadCompleta.nombre,
      nino_id: this.ninoSeleccionado,
      nino_nombre: ninoNombre
    });
    
    // Agregar a la lista de asignadas
    this.actividadesAsignadas.push(actividadCompleta);
    
    // Guardar en localStorage con el ID del niño
    const storageKey = `actividades_asignadas_${this.ninoSeleccionado}`;
    const asignadasActuales = localStorage.getItem(storageKey);
    let listaAsignadas = [];
    
    if (asignadasActuales) {
      try {
        listaAsignadas = JSON.parse(asignadasActuales);
      } catch (e) {
        console.error('Error parseando asignadas:', e);
      }
    }
    
    // Evitar duplicados
    if (!listaAsignadas.some((a: any) => a.actividad_id === actividadCompleta.actividad_id)) {
      listaAsignadas.push(actividadCompleta);
      localStorage.setItem(storageKey, JSON.stringify(listaAsignadas));
      console.log(`💾 Guardado en localStorage: ${storageKey}`);
    }
    
    // Cerrar modal primero
    this.cerrarModalAsignar();
    
    // Luego mostrar mensaje
    this.mensaje = `✅ Actividad "${actividadCompleta.nombre}" asignada correctamente a ${ninoNombre}`;
    this.error = null;
    this.cdr.detectChanges();
    
    console.log('✨ Asignación completada');
  }
}
