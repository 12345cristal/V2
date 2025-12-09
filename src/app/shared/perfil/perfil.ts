import { Component, OnInit, HostListener, signal, effect } from '@angular/core';
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

  // Señales
  perfil = signal<PerfilUsuario | null>(null);
  cargando = signal(false);
  guardando = signal(false);
  mensajeExito = signal<string | null>(null);
  mensajeError = signal<string | null>(null);
  alertaConfirmacion = signal(false);
  dirtyState = signal(false);

  fotoUrl = signal<string | null>(null);
  fotoFile: File | null = null;
  cvFile: File | null = null;

  constructor(
    private fb: FormBuilder,
    private perfilService: PerfilService
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.cargarPerfil();

    // Cuando se carga un perfil real → el formulario ya no está sucio
    effect(() => {
      if (this.perfil()) {
        this.dirtyState.set(false);
      }
    });

    // Detectar cambios en formulario
    this.form.valueChanges.subscribe(() => this.dirtyState.set(true));
  }

  /* ==========================================
     EVITAR CERRAR PÁGINA CON CAMBIOS SIN GUARDAR
  ========================================== */
  @HostListener('window:beforeunload', ['$event'])
  onBeforeUnload(e: BeforeUnloadEvent) {
    if (this.dirtyState()) {
      e.preventDefault();
      e.returnValue = true;
    }
  }

  /* =============================
        Inicializar Formulario
  ============================= */
  private initForm(): void {
    this.form = this.fb.group({
      telefono_personal: ['', Validators.required],
      correo_personal: ['', [Validators.required, Validators.email]],

      grado_academico: ['', Validators.required],
      especialidades: ['', Validators.required],
      experiencia: ['', Validators.required],

      domicilio_calle: ['', Validators.required],
      domicilio_colonia: ['', Validators.required],
      domicilio_cp: ['', Validators.required],
      domicilio_municipio: ['', Validators.required],
      domicilio_estado: ['', Validators.required]
    });
  }

  /* =============================
        Cargar Información Perfil
  ============================= */
  private cargarPerfil(): void {
    this.cargando.set(true);

    this.perfilService.getMiPerfil().subscribe({
      next: (perfilData) => {
        this.perfil.set(perfilData);

        // Foto existente
        if (perfilData.foto_perfil) {
          this.fotoUrl.set(perfilData.foto_perfil);
        }

        // Rellenar formulario
        this.form.patchValue({
          telefono_personal: perfilData.telefono_personal || '',
          correo_personal: perfilData.correo_personal || '',
          grado_academico: perfilData.grado_academico || '',
          especialidades: perfilData.especialidades || '',
          experiencia: perfilData.experiencia || '',
          domicilio_calle: perfilData.domicilio_calle || '',
          domicilio_colonia: perfilData.domicilio_colonia || '',
          domicilio_cp: perfilData.domicilio_cp || '',
          domicilio_municipio: perfilData.domicilio_municipio || '',
          domicilio_estado: perfilData.domicilio_estado || ''
        });

        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
        this.mensajeError.set('No se pudo cargar tu perfil.');
      }
    });
  }

  /* =============================
        Subir Foto Perfil
  ============================= */
  onFotoChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const file = input.files[0];

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

  /* =============================
        Subir CV (PDF)
  ============================= */
  onCvChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const file = input.files[0];

    if (file.type !== 'application/pdf') {
      this.mensajeError.set('Solo se permiten archivos PDF.');
      return;
    }

    this.cvFile = file;
    this.dirtyState.set(true);
  }

  /* =============================
        Mostrar modal de confirmación
  ============================= */
  intentarGuardar() {
    if (this.form.invalid) {
      this.mensajeError.set('Completa los campos obligatorios.');
      return;
    }

    if (!this.dirtyState()) {
      this.mensajeError.set('No hay cambios por guardar.');
      return;
    }

    this.alertaConfirmacion.set(true);
  }

  cancelarGuardado() {
    this.alertaConfirmacion.set(false);
  }

  /* =============================
        Guardar Perfil Final
  ============================= */
  guardarPerfil(): void {
    if (!this.perfil()) return;

    const fd = new FormData();

    // Convertir valores a string para evitar error TS2769
    Object.entries(this.form.value).forEach(([key, val]) => {
      let value = val;

      if (value === null || value === undefined) {
        value = '';
      }

      fd.append(key, String(value));
    });

    if (this.fotoFile) {
      fd.append('foto_perfil', this.fotoFile);
    }

    if (this.cvFile) {
      fd.append('cv_archivo', this.cvFile);
    }

    this.guardando.set(true);
    this.alertaConfirmacion.set(false);

    this.perfilService.actualizarMiPerfil(fd).subscribe({
      next: (perfilActualizado) => {
        this.perfil.set(perfilActualizado);
        this.guardando.set(false);
        this.mensajeExito.set('Perfil actualizado correctamente.');
        this.dirtyState.set(false);
      },
      error: () => {
        this.guardando.set(false);
        this.mensajeError.set('Ocurrió un error al guardar.');
      }
    });
  }
}
