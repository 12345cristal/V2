import {
  Component,
  HostListener,
  signal,
  effect,
  inject,
  Injector,
  runInInjectionContext
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

import { PerfilService } from '../../service/perfil.service';
import { PerfilUsuario } from '../../interfaces/perfil-usuario.interface';

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './perfil.html',
  styleUrls: ['./perfil.scss'],
})
export class PerfilComponent {

  private fb = inject(FormBuilder);
  private injector = inject(Injector);
  private perfilService = inject(PerfilService);

  // SIGNALS
  perfil = signal<PerfilUsuario | null>(null);
  cargando = signal(true);
  guardando = signal(false);
  dirtyState = signal(false);

  fotoUrl = signal<string | null>(null);
  fotoFile: File | null = null;
  cvFile: File | null = null;

  mensajeExito = signal<string | null>(null);
  mensajeError = signal<string | null>(null);
  alertaConfirmacion = signal(false);

  // FORMULARIO
  form = this.fb.group({
    telefono_personal: ['', Validators.required],
    correo_personal: ['', [Validators.required, Validators.email]],
    grado_academico: ['', Validators.required],
    especialidades: ['', Validators.required],
    experiencia: ['', Validators.required],
    domicilio_calle: ['', Validators.required],
    domicilio_colonia: ['', Validators.required],
    domicilio_cp: ['', Validators.required],
    domicilio_municipio: ['', Validators.required],
    domicilio_estado: ['', Validators.required],
  });

  constructor() {
    // EFFECT SIN ROMPER EL CICLO DE DETECCIÓN
    runInInjectionContext(this.injector, () => {
      effect(() => {
        if (this.perfil()) this.dirtyState.set(false);
      });
    });

    this.cargarPerfil();

    this.form.valueChanges.subscribe(() => {
      if (!this.cargando()) this.dirtyState.set(true);
    });
  }

  // ================================
  // CARGAR PERFIL
  // ================================
  cargarPerfil() {
    this.cargando.set(true);

    this.perfilService.getMiPerfil().subscribe({
      next: (data) => {
        this.perfil.set(data);

        this.fotoUrl.set(data.foto_perfil ?? null);

        this.form.patchValue({
          telefono_personal: data.telefono_personal,
          correo_personal: data.correo_personal,
          grado_academico: data.grado_academico ?? '',
          especialidades: data.especialidades ?? '',
          experiencia: data.experiencia ?? '',
          domicilio_calle: data.domicilio_calle ?? '',
          domicilio_colonia: data.domicilio_colonia ?? '',
          domicilio_cp: data.domicilio_cp ?? '',
          domicilio_municipio: data.domicilio_municipio ?? '',
          domicilio_estado: data.domicilio_estado ?? '',
        });

        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
        this.mensajeError.set('No se pudo cargar tu perfil.');
        setTimeout(() => this.mensajeError.set(null), 3000);
      },
    });
  }

  // ================================
  // FOTO
  // ================================
  abrirSelectorFoto(input: HTMLInputElement) {
    input.click();
  }

  onFotoChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      this.mensajeError.set('Solo se permiten imágenes.');
      return;
    }

    this.fotoFile = file;

    const reader = new FileReader();
    reader.onload = () => this.fotoUrl.set(reader.result as string);
    reader.readAsDataURL(file);

    this.dirtyState.set(true);
  }

  // ================================
  // CV
  // ================================
  onCvChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
      this.mensajeError.set('Solo se permiten PDFs.');
      return;
    }

    this.cvFile = file;
    this.dirtyState.set(true);
  }

  // ================================
  // GUARDAR
  // ================================
  intentarGuardar() {
    if (this.form.invalid) {
      this.mensajeError.set('Completa los campos obligatorios.');
      return;
    }
    this.alertaConfirmacion.set(true);
  }

  cancelarGuardado() {
    this.alertaConfirmacion.set(false);
  }

  guardarPerfil() {
    const fd = new FormData();

    Object.entries(this.form.value).forEach(([key, val]) => {
      fd.append(key, val ?? '');
    });

    if (this.fotoFile) fd.append('foto_perfil', this.fotoFile);
    if (this.cvFile) fd.append('cv_archivo', this.cvFile);

    this.guardando.set(true);

    this.perfilService.actualizarMiPerfil(fd).subscribe({
      next: (perfilActualizado) => {
        this.perfil.set(perfilActualizado);
        this.guardando.set(false);
        this.mensajeExito.set('Perfil actualizado correctamente.');
        this.dirtyState.set(false);

        setTimeout(() => this.mensajeExito.set(null), 3000);
      },
      error: () => {
        this.guardando.set(false);
        this.mensajeError.set('Error al guardar los cambios.');
        setTimeout(() => this.mensajeError.set(null), 3000);
      },
    });
  }

  // ================================
  // PREVENIR SALIDA
  // ================================
  @HostListener('window:beforeunload', ['$event'])
  onBeforeUnload(e: BeforeUnloadEvent) {
    if (this.dirtyState()) {
      e.preventDefault();
      e.returnValue = true;
    }
  }
}
