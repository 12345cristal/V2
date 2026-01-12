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
  data!: InicioPadre;
  cargando = true;

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

    this.inicioService.obtenerInicio(hijoId).subscribe({
      next: res => {
        this.data = res;
        this.cargando = false;
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  formatearFecha(fecha: string): string {
    return new Date(fecha).toLocaleDateString('es-MX', {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
    });
  }
}
