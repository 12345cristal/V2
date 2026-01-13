import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

interface Nino {
  id: number;
  nombre: string;
  apellido_paterno: string;
  apellido_materno: string;
  fecha_nacimiento: string;
  sexo: string;
  curp: string;
  estado: string;
  fecha_registro: string;
  diagnostico?: any;
  direccion?: any;
  info_emocional?: any;
  tutor?: any;
}

interface PerfilVectorizado {
  id: number;
  nino_id: number;
  edad: number;
  diagnosticos: string[];
  dificultades: string[];
  fortalezas: string[];
  texto_perfil: string;
  fecha_generacion: string;
  fecha_actualizacion: string;
}

interface ActividadAsignada {
  actividad_id: number;
  nombre: string;
  descripcion: string;
  area_desarrollo: string;
  dificultad: number;
  duracion_minutos: number;
  score: number;
  ranking: number;
  razon: string;
  fecha_asignacion: string;
  completada?: boolean;  // Nueva propiedad
}

interface RecomendacionHistorial {
  id: number;
  actividades_recomendadas: any[];
  metodo: string;
  fecha_generacion: string;
  aplicada: number;
}

@Component({
  selector: 'app-perfil-nino',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './perfil-nino.component.html',
  styleUrls: ['./perfil-nino.component.scss']
})
export class PerfilNinoComponent implements OnInit {
  private apiUrl = 'http://localhost:8000/api/v1';
  
  ninoId: number | null = null;
  nino: Nino | null = null;
  perfilVectorizado: PerfilVectorizado | null = null;
  actividadesAsignadas: ActividadAsignada[] = [];
  historialRecomendaciones: RecomendacionHistorial[] = [];
  
  cargando = true;
  error = '';
  
  // Modo edición
  modoEdicion = false;
  ninoEditado: any = {};
  
  // Tabs
  tabActiva: 'general' | 'perfil' | 'actividades' | 'historial' = 'general';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.ninoId = +params['id'];
      if (this.ninoId) {
        this.cargarDatosNino();
      }
    });
  }

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    });
  }

  cargarDatosNino(): void {
    this.cargando = true;
    this.error = '';

    // Cargar datos del niño
    this.http.get<Nino>(`${this.apiUrl}/ninos/${this.ninoId}`, { headers: this.getHeaders() })
      .subscribe({
        next: (data) => {
          this.nino = data;
          this.ninoEditado = { ...data };
          this.cargarPerfilVectorizado();
          this.cargarActividadesAsignadas();
          this.cargarHistorialRecomendaciones();
          this.cargando = false;
        },
        error: (err) => {
          console.error('Error al cargar niño:', err);
          this.error = 'No se pudo cargar la información del niño';
          this.cargando = false;
        }
      });
  }

  cargarPerfilVectorizado(): void {
    this.http.get<PerfilVectorizado>(
      `${this.apiUrl}/recomendaciones-actividades/perfil/${this.ninoId}`,
      { headers: this.getHeaders() }
    ).subscribe({
      next: (data) => {
        this.perfilVectorizado = data;
      },
      error: (err) => {
        console.error('Error al cargar perfil:', err);
      }
    });
  }

  cargarActividadesAsignadas(): void {
    // Obtener actividades asignadas desde localStorage o API
    const asignadas = localStorage.getItem(`actividades_asignadas_${this.ninoId}`);
    if (asignadas) {
      this.actividadesAsignadas = JSON.parse(asignadas);
    }
  }

  cargarHistorialRecomendaciones(): void {
    this.http.get<RecomendacionHistorial[]>(
      `${this.apiUrl}/recomendaciones-actividades/historial/${this.ninoId}`,
      { headers: this.getHeaders() }
    ).subscribe({
      next: (data) => {
        this.historialRecomendaciones = data;
      },
      error: (err) => {
        console.error('Error al cargar historial:', err);
      }
    });
  }

  calcularEdad(fechaNacimiento: string): number {
    if (!fechaNacimiento) return 0;
    const hoy = new Date();
    const nacimiento = new Date(fechaNacimiento);
    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    const mes = hoy.getMonth() - nacimiento.getMonth();
    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
      edad--;
    }
    return edad;
  }

  cambiarTab(tab: 'general' | 'perfil' | 'actividades' | 'historial'): void {
    this.tabActiva = tab;
  }

  activarEdicion(): void {
    if (this.nino?.estado === 'INACTIVO') {
      alert('No se puede editar un niño inactivo. Debe activarlo primero.');
      return;
    }
    this.modoEdicion = true;
    this.ninoEditado = { ...this.nino };
  }

  cancelarEdicion(): void {
    this.modoEdicion = false;
    this.ninoEditado = { ...this.nino };
  }

  guardarCambios(): void {
    if (!this.ninoId) return;

    this.http.put(
      `${this.apiUrl}/ninos/${this.ninoId}`,
      this.ninoEditado,
      { headers: this.getHeaders() }
    ).subscribe({
      next: (data) => {
        this.nino = data as Nino;
        this.modoEdicion = false;
        alert('Información actualizada correctamente');
      },
      error: (err) => {
        console.error('Error al actualizar:', err);
        alert('Error al actualizar la información');
      }
    });
  }

  getNivelDificultadTexto(nivel: number): string {
    const niveles: { [key: number]: string } = {
      1: 'Baja',
      2: 'Media',
      3: 'Alta'
    };
    return niveles[nivel] || 'Desconocida';
  }

  getNivelDificultadClase(nivel: number): string {
    const clases: { [key: number]: string } = {
      1: 'dificultad-baja',
      2: 'dificultad-media',
      3: 'dificultad-alta'
    };
    return clases[nivel] || '';
  }

  getAreaClase(area: string): string {
    const clases: { [key: string]: string } = {
      'motor': 'area-motor',
      'cognitivo': 'area-cognitivo',
      'social': 'area-social',
      'comunicacion': 'area-comunicacion',
      'sensorial': 'area-sensorial'
    };
    return clases[area] || 'area-default';
  }

  irARecomendaciones(): void {
    if (this.nino?.estado === 'INACTIVO') {
      alert('No se pueden asignar actividades a un niño inactivo. Debe activarlo primero.');
      return;
    }
    // Navegar con el ID del niño como parámetro de query
    this.router.navigate(['/coordinador/recomendaciones-actividades'], {
      queryParams: { ninoId: this.ninoId }
    });
  }

  volver(): void {
    this.router.navigate(['/coordinador/ninos']);
  }

  desasignarActividad(actividadId: number): void {
    if (this.nino?.estado === 'INACTIVO') {
      alert('No se pueden modificar actividades de un niño inactivo.');
      return;
    }
    if (!confirm('¿Desea desasignar esta actividad?')) return;

    this.actividadesAsignadas = this.actividadesAsignadas.filter(
      act => act.actividad_id !== actividadId
    );
    
    localStorage.setItem(
      `actividades_asignadas_${this.ninoId}`,
      JSON.stringify(this.actividadesAsignadas)
    );
  }

  toggleCompletada(actividadId: number): void {
    if (this.nino?.estado === 'INACTIVO') {
      alert('No se pueden modificar actividades de un niño inactivo.');
      return;
    }

    const actividad = this.actividadesAsignadas.find(
      act => act.actividad_id === actividadId
    );

    if (actividad) {
      actividad.completada = !actividad.completada;
      
      // Guardar en localStorage
      localStorage.setItem(
        `actividades_asignadas_${this.ninoId}`,
        JSON.stringify(this.actividadesAsignadas)
      );
      
      // Mensaje de confirmación
      const mensaje = actividad.completada 
        ? '✅ Actividad marcada como completada' 
        : '⏳ Actividad marcada como pendiente';
      alert(mensaje);
    }
  }

  generarReportePerfil(): void {
    window.print();
  }

  trackByIndex(_index: number): number {
    return _index;
  }

  trackByActividad(_index: number, item: ActividadAsignada): number {
    return item.actividad_id;
  }
}

