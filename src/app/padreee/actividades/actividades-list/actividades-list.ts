import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActividadAsignadaPadre } from '../../../interfaces/actividades-padre.interface';

@Component({
  selector: 'app-padre-actividades-list',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './actividades-list.html',
  styleUrls: ['./actividades-list.scss']
})
export class ActividadesListComponent {

  @Input() actividades: ActividadAsignadaPadre[] = [];
  @Input() seleccionada: ActividadAsignadaPadre | null = null;

  @Output() seleccionar = new EventEmitter<ActividadAsignadaPadre>();

  seleccionarActividad(a: ActividadAsignadaPadre) {
    this.seleccionar.emit(a);
  }

  esSeleccionada(a: ActividadAsignadaPadre) {
    return this.seleccionada && this.seleccionada.id === a.id;
  }
}
