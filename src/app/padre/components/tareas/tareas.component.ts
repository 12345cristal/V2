import { Component, signal, inject, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { TareasPadreService } from '../../../service/tareas-padre.service';
import { PadreHijosStateService } from '../../../service/padre-hijos-state.service';
import { TareaPadre } from '../../../interfaces/tarea.interface';
import { NotificacionesService } from '../../../service/notificaciones.service';

@Component({
  selector: 'app-tareas-padre',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './tareas.component.html',
  styleUrls: ['./tareas.component.scss'],
})
export class TareasPadreComponent {

  private service = inject(TareasPadreService);
  private hijosState = inject(PadreHijosStateService);
  private notificacionesService = inject(NotificacionesService);

  hijoId = this.hijosState.seleccionadoId;
  hijoNombre = signal<string>('');

  tareas = signal<TareaPadre[]>([]);
  cargando = signal(false);
  error = signal<string | null>(null);

  // Completar tarea
  tareaCompletandoId = signal<number | null>(null);
  observaciones = signal<string>('');
  archivoEvidencia = signal<File | null>(null);
  nombreArchivo = signal<string>('');
  completando = signal(false);

  constructor() {
    // Solicitar permiso para notificaciones
    this.notificacionesService.solicitarPermisoNotificaciones();

    effect(() => {
      const id = this.hijoId();
      const hijos = this.hijosState.hijos();

      if (id) {
        const hijo = hijos.find(h => h.id === id);
        if (hijo) {
          this.hijoNombre.set(hijo.nombre);
          this.cargar();
          
          // Conectar WebSocket para notificaciones
          this.notificacionesService.conectarWebSocket(id);
        }
      } else {
        this.error.set('Selecciona un hijo primero');
      }
    });
  }

  ngOnDestroy() {
    this.notificacionesService.desconectar();
  }

  cargar() {
    if (!this.hijoId()) return;

    this.cargando.set(true);
    this.error.set(null);

    this.service.getTareas(this.hijoId()!).subscribe({
      next: (t: TareaPadre[]) => {
        this.tareas.set(t);
        this.cargando.set(false);
      },
      error: (err: HttpErrorResponse | unknown) => {
        console.error(err);
        this.error.set('No se pudieron cargar las tareas');
        this.cargando.set(false);
      }
    });
  }

  iniciarCompletar(tareaId: number) {
    this.tareaCompletandoId.set(tareaId);
    this.observaciones.set('');
    this.archivoEvidencia.set(null);
    this.nombreArchivo.set('');
  }

  cancelarCompletar() {
    this.tareaCompletandoId.set(null);
    this.observaciones.set('');
    this.archivoEvidencia.set(null);
    this.nombreArchivo.set('');
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      
      // Validar tipo de archivo
      const tiposPermitidos = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
      if (!tiposPermitidos.includes(file.type)) {
        this.error.set('Solo se permiten archivos PDF o imágenes (JPG, PNG)');
        return;
      }

      // Validar tamaño (5MB máximo)
      if (file.size > 5 * 1024 * 1024) {
        this.error.set('El archivo no debe superar los 5MB');
        return;
      }

      this.archivoEvidencia.set(file);
      this.nombreArchivo.set(file.name);
      this.error.set(null);
    }
  }

  marcarComoRealizada() {
    const tareaId = this.tareaCompletandoId();
    if (!tareaId) return;

    this.completando.set(true);
    this.error.set(null);

    this.service
      .marcarRealizada(
        tareaId,
        this.observaciones() || undefined,
        this.archivoEvidencia() || undefined
      )
      .subscribe({
        next: (tareaActualizada: TareaPadre) => {
          // Actualizar lista
          this.tareas.set(
            this.tareas().map(t => (t.id === tareaId ? tareaActualizada : t))
          );
          this.completando.set(false);
          this.cancelarCompletar();
        },
        error: (err: HttpErrorResponse | unknown) => {
          console.error(err);
          this.error.set('No se pudo marcar la tarea como realizada');
          this.completando.set(false);
        }
      });
  }

  descargarRecurso(url: string, nombre: string) {
    this.service.descargarRecurso(url).subscribe({
      next: (blob: Blob) => {
        const urlBlob = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = urlBlob;
        a.download = nombre;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(urlBlob);
        document.body.removeChild(a);
      },
      error: (err: HttpErrorResponse | unknown) => {
        console.error(err);
        this.error.set('No se pudo descargar el recurso');
      }
    });
  }

  verArchivo(url: string) {
    window.open(url, '_blank');
  }

  esVencida(fechaLimite?: string): boolean {
    if (!fechaLimite) return false;
    return new Date(fechaLimite) < new Date();
  }
}
