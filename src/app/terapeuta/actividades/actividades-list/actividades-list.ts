import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActividadesService } from '../../../service/terapeuta/actividade-terapeuta.service';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-actividades-list',
  imports: [CommonModule, RouterModule],
  templateUrl: './actividades-list.html',
})
export class ActividadesListComponent {
  actividades$ = this.actividadesService.getActividadesPorTerapeuta();

  constructor(private actividadesService: ActividadesService) {}
}