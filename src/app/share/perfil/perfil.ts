import { Component, OnInit, HostListener, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { PerfilService } from '../../service/perfil.service';
import { PerfilUsuario } from '../../interfaces/perfil-usuario.interface';

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './perfil.html',
  styleUrls: ['./perfil.scss']
})
export class PerfilComponent implements OnInit {

  form!: FormGroup;
  perfil: PerfilUsuario | null = null;

  cargando = signal<boolean>(false);
  guardando = signal<boolean>(false);
  mensajeExito = signal<string | null>(null);
  mensajeError = signal<string | null>(null);
  alertaConfirmacion = signal<boolean>(false);

  cvFile: File | null = null;
  fotoUrl: string | null = null;

  // Detecta si hay cambios sin guardar
  dirtyState = signal<boolean>(false);

  constructor(
    private fb: FormBuilder,
    private perfilService: PerfilService
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.cargarPerfil();

    // Detectamos cambios para advertir al usuario
    this.form.valueChanges.subscribe(() => {
      if (this.perfil) {
        this.dirtyState.set(true);
      }
    });
  }

  /* =======================================
     PROTECCIÓN AL CERRAR LA PÁGINA
  ======================================= */
  @HostListener('window:beforeunload', ['$event'])
  onBeforeUnload(e: BeforeUnloadEvent) {
    if (this.dirtyState()) {
      e.preventDefault();
      e.returnValue = true;
    }
  }

  private initForm(): void {
    this.form = this.fb.group({
      telefono_personal: ['', [Validators.required]],
      correo_personal: ['', [Validators.required, Validators.email]],

      grado_academico: ['', Validators.required],
      especialidades: ['', Validators.required],
      experiencia: ['', [Validators.required, Validators.minLength(10)]],

      domicilio_calle: ['', Validators.required],
      domicilio_colonia: ['', Validators.required],
      domicilio_cp: ['', Validators.required],
      domicilio_municipio: ['', Validators.required],
      domicilio_estado: ['', Validators.required],
    });
  }

  private cargarPerfil(): void {
    this.cargando.set(true);
    this.mensajeError.set(null);

    this.perfilService.getMiPerfil().subscribe({
      next: (perfil) => {
        this.perfil = perfil;

        this.form.patchValue({
          telefono_personal: perfil.telefono_personal,
          correo_personal: perfil.correo_personal,
          grado_academico: perfil.grado_academico,
          especialidades: perfil.especialidades,
          experiencia: perfil.experiencia,
          domicilio_calle: perfil.domicilio_calle,
          domicilio_colonia: perfil.domicilio_colonia,
          domicilio_cp: perfil.domicilio_cp,
          domicilio_municipio: perfil.domicilio_municipio,
          domicilio_estado: perfil.domicilio_estado
        });

        this.cargando.set(false);
        this.dirtyState.set(false);
      },
      error: () => {
        this.mensajeError.set('No se pudo cargar tu perfil. Intenta más tarde.');
        this.cargando.set(false);
      }
    });
  }

  /* =======================================
     CAMBIO DE CV CON ALERTA
  ======================================= */
  onCvChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) {
      this.cvFile = null;
      return;
    }

    const file = input.files[0];

    if (file.type !== 'application/pdf') {
      this.mensajeError.set('Solo se permiten archivos PDF.');
      return;
    }

    if (file.size > 3 * 1024 * 1024) {
      this.mensajeError.set('El archivo es demasiado grande (máximo 3 MB).');
      return;
    }

    this.cvFile = file;
    this.mensajeExito.set('Archivo seleccionado correctamente.');
    this.dirtyState.set(true);
  }

  /* =======================================
     CONFIRMAR GUARDADO
  ======================================= */
  intentarGuardar() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      this.mensajeError.set('Corrige los campos en rojo antes de continuar.');
      return;
    }

    if (!this.dirtyState()) {
      this.mensajeError.set('No hay cambios para guardar.');
      return;
    }

    this.alertaConfirmacion.set(true);
  }

  cancelarGuardado() {
    this.alertaConfirmacion.set(false);
  }

  /* =======================================
     GUARDADO FINAL
  ======================================= */
  guardarPerfil(): void {
    if (!this.perfil) return;

    this.alertaConfirmacion.set(false);
    this.guardando.set(true);

    const formData = new FormData();
    for (const [key, value] of Object.entries(this.form.value)) {
      formData.append(key, value as string);
    }

    if (this.cvFile) {
      formData.append('cv_archivo', this.cvFile);
    }

    formData.append('id_personal', String(this.perfil.id_personal));

    this.perfilService.actualizarMiPerfil(formData).subscribe({
      next: (perfilActualizado) => {
        this.perfil = perfilActualizado;
        this.guardando.set(false);
        this.mensajeExito.set('Tu perfil se ha actualizado correctamente.');
        this.dirtyState.set(false);

        setTimeout(() => this.mensajeExito.set(null), 3000);
      },
      error: () => {
        this.guardando.set(false);
        this.mensajeError.set('Ocurrió un error al guardar los cambios.');
      }
    });
  }

  /* =======================================
     HELPERS
  ======================================= */
  tieneError(nombre: string, error: string) {
    const c = this.form.get(nombre);
    return c?.touched && c?.hasError(error);
  }
}
