import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { Observable } from 'rxjs';

import { ActividadesService } from '../../service/terapeuta/actividade-terapeuta.service';
import { Actividad } from '../../interfaces/terapeuta/actividad.interface';

@Component({
  selector: 'app-actividades',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './actividades.html',
  styleUrl: './actividades.scss',
})
export class Actividades {
  private actividadesSrv = inject(ActividadesService);

  actividades$!: Observable<Actividad[]>;

  // formulario
  nino_id!: number;
  titulo = '';
  descripcion = '';
  tipo: 'TAREA' | 'ARCHIVO' = 'TAREA';
  archivo?: File;

  ngOnInit() {
    this.actividades$ = this.actividadesSrv.listar();
  }

  onFileChange(e: Event) {
    const input = e.target as HTMLInputElement;
    if (input.files?.length) {
      this.archivo = input.files[0];
    }
  }

  guardar() {
    const fd = new FormData();
    fd.append('nino_id', String(this.nino_id));
    fd.append('titulo', this.titulo);
    fd.append('descripcion', this.descripcion);
    fd.append('tipo', this.tipo);

    if (this.archivo) {
      fd.append('archivo', this.archivo);
    }

    this.actividadesSrv.crear(fd).subscribe(() => {
      this.actividades$ = this.actividadesSrv.listar();
      this.titulo = '';
      this.descripcion = '';
      this.archivo = undefined;
    });
  }
}
