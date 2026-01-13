import { Component, signal, inject, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PagosPadreService } from '../../services/pagos-padre.service';
import { PlanPagoResumen } from '../../interfaces/pagos.interface';

@Component({
  selector: 'app-pagos-padre',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './pagos.component.html',
  styleUrls: ['./pagos.component.scss'],
})
export class PagosPadreComponent {

  private service = inject(PagosPadreService);

  hijoId = signal<number | null>(null);
  plan = signal<PlanPagoResumen | null>(null);

  cargando = signal(false);
  error = signal<string | null>(null);

  constructor() {
    effect(() => {
      if (this.hijoId()) {
        this.cargar();
      }
    });
  }

  cargar() {
    this.cargando.set(true);
    this.service.getResumen(this.hijoId()!).subscribe({
      next: r => {
        this.plan.set(r);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudo cargar la información de pagos');
        this.cargando.set(false);
      }
    });
  }

  descargarReporte() {
    this.service.descargarReporte(this.hijoId()!).subscribe(blob => {
      const url = URL.createObjectURL(blob);
      window.open(url);
    });
  }

  descargarComprobante(pagoId: number) {
    this.service.descargarComprobante(pagoId).subscribe(blob => {
      const url = URL.createObjectURL(blob);
      window.open(url);
    });
  }
}



