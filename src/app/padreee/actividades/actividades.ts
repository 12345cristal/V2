import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActividadesPadreService } from '../../service/actividades-padre.service';
import {
  ActividadAsignadaPadre,
  ResumenActividadesPadre
} from '../../interfaces/actividades-padre.interface';

import { ActividadesListComponent } from './actividades-list/actividades-list';
import { ActividadDetalleComponent } from './actividad-detalle/actividad-detalle';
import { from } from 'rxjs';

@Component({
  selector: 'app-padre-actividades',
  standalone: true,
  imports: [
    CommonModule,
    ActividadesListComponent,
    ActividadDetalleComponent
  ],
  templateUrl: './actividades.html',
  styleUrls: ['./actividades.scss']
})
export class PadreActividadesComponent implements OnInit {

  actividades: ActividadAsignadaPadre[] = [];
  resumen: ResumenActividadesPadre | null = null;

  cargando = false;
  seleccionada: ActividadAsignadaPadre | null = null;

  constructor(private actividadesPadreService: ActividadesPadreService) {}

  ngOnInit(): void {
    this.cargarDatos();
  }

  cargarDatos() {
    this.cargando = true;

    this.actividadesPadreService.getMisActividades().subscribe(list => {
      this.actividades = list;
      this.resumen = this.calcularResumen(list);
      this.cargando = false;

      // Si no hay seleccionada, por defecto la primera pendiente
      if (!this.seleccionada && list.length > 0) {
        const pendiente = list.find(a => !a.completado);
        this.seleccionada = pendiente ?? list[0];
      }
    });
  }

  private calcularResumen(list: ActividadAsignadaPadre[]): ResumenActividadesPadre {
    const hoy = new Date();
    const soloFecha = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime();

    const hoyMs = soloFecha(hoy);

    let totalPendientes = 0;
    let totalCompletadas = 0;
    let pendientesHoy = 0;

    for (const a of list) {
      if (a.completado) {
        totalCompletadas++;
      } else {
        totalPendientes++;
        if (a.fechaLimite) {
          const fechaLimite = new Date(a.fechaLimite);
          if (soloFecha(fechaLimite) === hoyMs) {
            pendientesHoy++;
          }
        }
      }
    }

    return {
      totalPendientes,
      totalCompletadas,
      pendientesHoy
    };
  }

  // Evento que viene del listado
  onSeleccionar(asignacion: ActividadAsignadaPadre) {
    this.seleccionada = asignacion;
  }

  // Cuando el detalle actualiza algo, refrescamos listado + resumen
  onActualizado() {
    this.cargarDatos();
  }
}

