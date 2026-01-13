import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
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

  constructor(private inicioService: InicioTerapeutaService) {
    this.cargar();
  }

  cargar() {
    this.cargando = true;
    this.inicioService.getDashboard().subscribe({
      next: res => (this.data = res),
      complete: () => (this.cargando = false),
    });
  }

  trackById(_: number, item: any) {
    return item?.id;
  }
}
