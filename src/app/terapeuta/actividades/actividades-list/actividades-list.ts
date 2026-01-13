import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Observable } from 'rxjs';

import { ActividadesService } from '../../../service/terapeuta/actividade-terapeuta.service';
import { ActividadAsignada } from '../../../interfaces/terapeuta/actividad-asignada.interface';

@Component({
  standalone: true,
  selector: 'app-actividades-list',
  imports: [
    CommonModule,
    RouterModule   // 👈 OBLIGATORIO para routerLink
  ],
  templateUrl: './actividades-list.html',
  styleUrls: ['./actividades-list.scss'],
})
export class ActividadesList implements OnInit {

  actividades$!: Observable<ActividadAsignada[]>;

  constructor(private actividadesService: ActividadesService) {}

  ngOnInit(): void {
    this.actividades$ = this.actividadesService.getActividadesPorTerapeuta();
  }
}
