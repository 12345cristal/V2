import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { MisHijosService, HijoCreateDto, HijoUpdateDto } from '../../../service/mis-hijos.service';
import { PadreHijosStateService } from '../../../service/padre-hijos-state.service';
import { Hijo } from '../../../interfaces/hijo.interface';
import { HttpErrorResponse } from '@angular/common/http';

type HijoUpsert = {
  nombre: string;
  edad: number | null;
  fechaNacimiento: string | null;
  avatar: string | null;
  diagnostico: string | null;
};

@Component({
  selector: 'app-mis-hijos',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './mis-hijos.component.html',
  styleUrls: ['./mis-hijos.component.scss']
})
export class MisHijosComponent {
  private service = inject(MisHijosService);
  private state = inject(PadreHijosStateService);
  private fb = inject(FormBuilder);

  hijos = signal<Hijo[]>([]);
  cargando = signal<boolean>(true);
  error = signal<string | null>(null);
  editandoId = signal<number | null>(null);

  form = this.fb.group({
    nombre: ['', [Validators.required, Validators.minLength(2)]],
    edad: [null as number | null],
    fechaNacimiento: [null as string | null],
    avatar: [null as string | null],
    diagnostico: [null as string | null]
  });

  constructor() {
    this.cargarHijos();
  }

  private toCreateDto(v: HijoUpsert): HijoCreateDto {
    return {
      nombre: v.nombre.trim(),
      edad: v.edad ?? undefined,
      fechaNacimiento: v.fechaNacimiento || undefined,
      avatar: v.avatar || undefined,
      diagnostico: v.diagnostico || undefined
    };
  }

  private toUpdateDto(v: HijoUpsert): HijoUpdateDto {
    return {
      nombre: v.nombre?.trim() || undefined,
      edad: v.edad ?? undefined,
      fechaNacimiento: v.fechaNacimiento || undefined,
      avatar: v.avatar || undefined,
      diagnostico: v.diagnostico || undefined
    };
  }

  cargarHijos() {
    this.cargando.set(true);
    this.service.getHijos().subscribe({
      next: (lista: Hijo[]) => {
        this.hijos.set(lista);
        this.state.setHijos(lista);
        this.error.set(null);
        this.cargando.set(false);
      },
      error: (err: HttpErrorResponse | unknown) => {
        console.error(err);
        this.error.set('No se pudieron cargar los hijos');
        this.cargando.set(false);
      }
    });
  }

  iniciarCrear() {
    this.editandoId.set(null);
    this.form.reset();
  }

  iniciarEditar(hijo: Hijo) {
    this.editandoId.set(hijo.id);
    this.form.reset({
      nombre: hijo.nombre ?? '',
      edad: hijo.edad ?? null,
      fechaNacimiento: (hijo.fechaNacimiento as string) ?? null,
      avatar: hijo.avatar ?? null,
      diagnostico: hijo.diagnostico ?? null
    });
  }

  cancelarEdicion() {
    this.editandoId.set(null);
    this.form.reset();
  }

  guardar() {
    if (this.form.invalid) return;
    const upsert = this.form.getRawValue() as HijoUpsert;

    if (this.editandoId() === null) {
      const dto = this.toCreateDto(upsert);
      this.service.createHijo(dto).subscribe({
        next: (nuevo: Hijo) => {
          this.hijos.set([nuevo, ...this.hijos()]);
          this.state.addHijo(nuevo);
          this.form.reset();
          this.error.set(null);
        },
        error: (err: HttpErrorResponse | unknown) => {
          console.error(err);
          this.error.set('No se pudo crear el hijo');
        }
      });
    } else {
      const id = this.editandoId()!;
      const patch = this.toUpdateDto(upsert);
      this.service.updateHijo(id, patch).subscribe({
        next: (actualizado: Hijo) => {
          this.hijos.set(this.hijos().map(h => (h.id === id ? actualizado : h)));
          this.state.updateHijo(actualizado);
          this.cancelarEdicion();
          this.error.set(null);
        },
        error: (err: HttpErrorResponse | unknown) => {
          console.error(err);
          this.error.set('No se pudo actualizar el hijo');
        }
      });
    }
  }

  eliminar(id: number) {
    if (!confirm('¿Eliminar este hijo?')) return;
    this.service.deleteHijo(id).subscribe({
      next: () => {
        this.hijos.set(this.hijos().filter(h => h.id !== id));
        this.state.removeHijo(id);
        this.error.set(null);
      },
      error: (err: HttpErrorResponse | unknown) => {
        console.error(err);
        this.error.set('No se pudo eliminar el hijo');
      }
    });
  }
}
