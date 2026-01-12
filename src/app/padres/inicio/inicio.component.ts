import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InicioService } from '../services/inicio.service';
import { InicioPadre } from '../interfaces/inicio.interface';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.scss'],
})
export class InicioComponent implements OnInit {

  saludo = '';
  data: InicioPadre | null = null;
  cargando = true;
  error: string | null = null;

  constructor(private inicioService: InicioService) {}

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
      next: res => {
        this.data = res;
        this.cargando = false;
      },
      error: () => {
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
      day: 'numeric'
    });
  }

  cambiarHijo(hijoId: string): void {
    this.cargarInicio(hijoId);
  }
}
