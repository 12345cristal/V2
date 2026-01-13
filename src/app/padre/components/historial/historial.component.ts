import { Component, signal, inject, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpErrorResponse } from '@angular/common/http';
import { HistorialPadreService } from '../../../service/historial-padre.service';
import { PadreHijosStateService } from '../../../service/padre-hijos-state.service';
import { HistorialResumen } from '../../../interfaces/historial.interface';

@Component({
  selector: 'app-historial-padre',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './historial.component.html',
  styleUrls: ['./historial.component.scss'],
})
export class HistorialPadreComponent {

  private service = inject(HistorialPadreService);
  private hijosState = inject(PadreHijosStateService);

  hijoId = this.hijosState.seleccionadoId; // sincronizado
  hijoNombre = signal<string>('');

  resumen = signal<HistorialResumen | null>(null);
  cargando = signal(false);
  error = signal<string | null>(null);

  constructor() {
    effect(() => {
      const id = this.hijoId();
      const hijos = this.hijosState.hijos();
      
      if (id) {
        const hijo = hijos.find(h => h.id === id);
        if (hijo) {
          this.hijoNombre.set(hijo.nombre);
          this.cargar();
        }
      } else {
        this.error.set('Selecciona un hijo primero');
      }
    });
  }

  cargar() {
    if (!this.hijoId()) return;

    this.cargando.set(true);
    this.error.set(null);

    this.service.getResumen(this.hijoId()!).subscribe({
      next: (r: HistorialResumen) => {
        this.resumen.set(r);
        this.cargando.set(false);
      },
      error: (err: HttpErrorResponse | unknown) => {
        console.error(err);
        this.error.set('No se pudo cargar el historial');
        this.cargando.set(false);
      }
    });
  }

  descargarPDF() {
    if (!this.hijoId()) {
      this.error.set('Selecciona un hijo primero');
      return;
    }

    this.service.descargarReporte(this.hijoId()!).subscribe({
      next: (blob: Blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `historial-${this.hijoNombre()}-${new Date().getTime()}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      },
      error: (err: HttpErrorResponse | unknown) => {
        console.error(err);
        this.error.set('No se pudo descargar el reporte');
      }
    });
  }
}



