import { Component } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { RouterModule } from '@angular/router';
import { InicioTerapeutaService, TerapeutaDashboard } from '../../service/terapeuta/inicio-terapeuta.service';

@Component({
  standalone: true,
  selector: 'app-inicio-terapeuta',
  imports: [CommonModule, RouterModule],
  templateUrl: './inicio.html',
  styleUrls: ['./inicio.scss'],
})
export class InicioTerapeuta {
  data?: TerapeutaDashboard;
  cargando = true;

  // Colores para avatares
  private readonly colores = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
    '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B88B', '#52D0B3'
  ];

  constructor(private inicioService: InicioTerapeutaService) {
    this.cargar();
  }

  cargar() {
    this.cargando = true;
    this.inicioService.getDashboard().subscribe({
      next: res => {
        this.data = res;
      },
      complete: () => (this.cargando = false),
    });
  }

  trackById(_: number, item: any) {
    return item?.id;
  }

  getHoy(): string {
    const hoy = new Date();
    const dias = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
    const meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                   'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
    
    const diaNombre = dias[hoy.getDay()];
    const diaNum = hoy.getDate();
    const mesNombre = meses[hoy.getMonth()];
    const anio = hoy.getFullYear();
    
    return `${diaNombre}, ${diaNum} de ${mesNombre} ${anio}`;
  }

  getColorByIndex(index: number): string {
    return this.colores[index % this.colores.length];
  }
}
