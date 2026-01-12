import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { InicioService } from '../../service/padres/inicio.service';
import { InicioPadre } from '../../interfaces/padres/inicio.interface';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule, FormsModule], // ← FormsModule es OBLIGATORIO para ngModel
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.scss'],
})
export class InicioComponent implements OnInit {
  
  saludo = '';
  data: InicioPadre | null = null;
  cargando = true;
  error: string | null = null;
  hijoSeleccionadoId = '';

  private inicioService = inject(InicioService);

  ngOnInit(): void {
    this.generarSaludo();
    this.cargarInicio();
  }

  private generarSaludo(): void {
    const hora = new Date().getHours();
    if (hora < 12) this.saludo = 'Buenos días';
    else if (hora < 18) this.saludo = 'Buenas tardes';
    else this.saludo = 'Buenas noches';
  }

  cargarInicio(hijoId?: string): void {
    this.cargando = true;
    this.error = null;

    this.inicioService.obtenerInicio(hijoId).subscribe({
      next: (res) => {
        this.data = res;
        this.cargando = false;
      },
      error: (err) => {
        console.error('Error al cargar inicio:', err);
        this.error = 'Error al cargar los datos';
        this.cargando = false;
      }
    });
  }

  formatearFecha(fecha: string | Date): string {
    const f = typeof fecha === 'string' ? new Date(fecha) : fecha;
    return f.toLocaleDateString('es-MX', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  cambiarHijo(hijoId: string): void {
    if (hijoId) {
      this.cargarInicio(hijoId);
    }
  }
}
