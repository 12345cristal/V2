import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RecursosService } from '../../service/terapeuta/recursos.service';

@Component({
  standalone: true,
  selector: 'app-recurso-upload',
  imports: [CommonModule, FormsModule],
  templateUrl: './recursos-upload.html',
  styleUrls: ['./recursos-upload.scss'],
})
export class RecursoUploadComponent {

  @Input() ninoId?: number; // si viene, se asigna como tarea

  titulo = '';
  descripcion = '';
  tipoId!: number;
  categoriaId?: number;
  nivelId?: number;
  archivo?: File;

  cargando = false;

  constructor(private recursosService: RecursosService) {}

  onFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) {
      this.archivo = input.files[0];
    }
  }

  subir() {
    if (!this.archivo || !this.titulo || !this.tipoId) {
      alert('Completa los campos obligatorios');
      return;
    }

    const formData = new FormData();
    formData.append('titulo', this.titulo);
    formData.append('descripcion', this.descripcion);
    formData.append('tipo_id', String(this.tipoId));
    if (this.categoriaId) formData.append('categoria_id', String(this.categoriaId));
    if (this.nivelId) formData.append('nivel_id', String(this.nivelId));
    formData.append('archivo', this.archivo);

    this.cargando = true;

    this.recursosService.crearRecurso(formData).subscribe({
      next: recurso => {
        // si viene ninoId → asignar como tarea
        if (this.ninoId) {
          this.recursosService.asignarRecursoANino({
            recurso_id: recurso.id,
            nino_id: this.ninoId,
          }).subscribe(() => alert('Recurso asignado al niño'));
        } else {
          alert('Recurso subido correctamente');
        }

        this.reset();
      },
      complete: () => (this.cargando = false),
    });
  }

  reset() {
    this.titulo = '';
    this.descripcion = '';
    this.tipoId = undefined as any;
    this.categoriaId = undefined;
    this.nivelId = undefined;
    this.archivo = undefined;
  }
}
