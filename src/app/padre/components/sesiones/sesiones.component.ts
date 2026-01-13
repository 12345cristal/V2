import { Component, signal, inject, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { SesionesPadreService } from '../../../service/sesiones-padre.service';
import { PadreHijosStateService } from '../../../service/padre-hijos-state.service';
import { Sesion, SesionDetalle } from '../../../interfaces/sesiones.interface';

type Vista = 'HOY' | 'PROGRAMADAS' | 'SEMANA';

@Component({
  selector: 'app-sesiones-padre',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sesiones.component.html',
  styleUrls: ['./sesiones.component.scss'],
})
export class SesionesPadreComponent {

  private service = inject(SesionesPadreService);
  private hijosState = inject(PadreHijosStateService);

  hijoId = this.hijosState.seleccionadoId; // compartido
  hijoNombre = signal<string>('');

  vista = signal<Vista>('HOY');
  sesiones = signal<Sesion[]>([]);
  detalle = signal<SesionDetalle | null>(null);

  cargando = signal(false);
  error = signal<string | null>(null);

  constructor() {
    // Sincroniza cambios de hijo y carga automáticamente sesiones
    effect(() => {
      const id = this.hijoId();
      const hijos = this.hijosState.hijos();
      
      if (id) {
        const hijo = hijos.find(h => h.id === id);
        if (hijo) {
          this.hijoNombre.set(hijo.nombre);
          this.cargar('HOY'); // carga automáticamente
        }
      }
    });
  }

  cargar(vista: Vista) {
    if (!this.hijoId()) {
      this.error.set('Selecciona un hijo primero');
      return;
    }

    this.vista.set(vista);
    this.cargando.set(true);
    this.error.set(null);

    const request =
      vista === 'HOY'
        ? this.service.getHoy(this.hijoId()!)
        : vista === 'PROGRAMADAS'
        ? this.service.getProgramadas(this.hijoId()!)
        : this.service.getSemana(this.hijoId()!);

    request.subscribe({
      next: (data: Sesion[]) => {
        this.sesiones.set(data);
        this.cargando.set(false);
      },
      error: (err: HttpErrorResponse | unknown) => {
        console.error(err);
        this.error.set('No se pudieron cargar las sesiones');
        this.cargando.set(false);
      }
    });
  }

  verDetalle(id: number) {
    this.service.getDetalle(id).subscribe({
      next: (d: SesionDetalle) => {
        this.detalle.set(d);
        this.error.set(null);
      },
      error: (err: HttpErrorResponse | unknown) => {
        console.error(err);
        this.error.set('No se pudo cargar el detalle');
      }
    });
  }

  cerrarDetalle() {
    this.detalle.set(null);
  }

  descargarBitacora(id: number) {
    this.service.descargarBitacora(id).subscribe({
      next: (blob: Blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `bitacora-sesion-${id}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      },
      error: (err: HttpErrorResponse | unknown) => {
        console.error(err);
        this.error.set('No se pudo descargar la bitácora');
      }
    });
  }
}



