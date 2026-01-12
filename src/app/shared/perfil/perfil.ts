import {
  Component,
  HostListener,
  signal,
  effect,
  inject,
  Injector,
  runInInjectionContext,
  OnDestroy,
  DestroyRef,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators, FormsModule } from '@angular/forms';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { finalize } from 'rxjs/operators';
import { MatIconModule } from '@angular/material/icons';
import { MatButtonModule } from '@angular/material/button';

import { PerfilService } from '../../service/perfil.service';
import { PerfilUsuario } from '../../interfaces/perfil-usuario.interface';
import { ArchivosService } from '../../service/archivos.service';
import { PdfViewerComponent } from './pdf-viewer.component';

type ToastTipo = 'success' | 'error';

type DocPreview = {
  name: string;
  type: string;
  rawUrl: string;            // blob:...
  safeUrl: SafeResourceUrl;  // para iframe
};

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    PdfViewerComponent,
    MatIconModule,
    MatButtonModule,
  ],
  templateUrl: './perfil.html',
  styleUrls: ['./perfil.scss'],
})
export class PerfilComponent implements OnDestroy {
  // ================================
  // DEPENDENCIAS
  // ================================
  private fb = inject(FormBuilder);
  private injector = inject(Injector);
  private perfilService = inject(PerfilService);
  private archivosService = inject(ArchivosService);
  private sanitizer = inject(DomSanitizer);
  private destroyRef = inject(DestroyRef);

  // ================================
  // SIGNALS
  // ================================
  perfil = signal<PerfilUsuario | null>(null);

  cargando = signal(true);
  guardando = signal(false);
  dirtyState = signal(false);

  fotoUrl = signal<string | null>(null);
  alertas = signal<string[]>([]);

  mostrarToast = signal(false);
  toastTipo = signal<ToastTipo>('success');
  toastMensaje = signal('');

  mostrarModalConfirmar = signal(false);
  mostrarModalPassword = signal(false);

  // ================================
  // ARCHIVOS (Files)
  // ================================
  fotoFile: File | null = null;
  cvFile: File | null = null;
  documentosExtras: File[] = [];

  // ================================
  // VISOR PROPIO (blob urls)
  // ================================
  cvSafeUrl = signal<SafeResourceUrl | null>(null);
  cvRawUrl = signal<string | null>(null);
  cvNombre = signal<string>('curriculum.pdf');

  docsPreviews = signal<DocPreview[]>([]);

  // guardamos TODOS los raw urls para revocarlos
  private allocatedObjectUrls = new Set<string>();

  // ================================
  // PASSWORD
  // ================================
  passwordActual = '';
  passwordNueva = '';
  passwordConfirmar = '';

  // ================================
  // FORM
  // ================================
  form = this.fb.group({
    telefono_personal: [''],
    correo_personal: ['', [Validators.email]],
    grado_academico: [''],
    especialidades: [''],
    experiencia: [''],
    domicilio_calle: [''],
    domicilio_colonia: [''],
    domicilio_cp: [''],
    domicilio_municipio: [''],
    domicilio_estado: [''],
  });

  constructor() {
    // Reset dirty cuando cambia perfil
    runInInjectionContext(this.injector, () => {
      effect(() => {
        if (this.perfil()) {
          this.dirtyState.set(false);
          this.generarAlertas();
        }
      });
    });

    this.cargarPerfil();

    this.form.valueChanges
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(() => {
        if (!this.cargando()) this.dirtyState.set(true);
      });
  }

  // ================================
  // CARGAR PERFIL + LIMPIEZA
  // ================================
  cargarPerfil() {
    this.cargando.set(true);

    // 🧼 limpiar previews cada vez que recargas perfil
    this.resetVisoresYUrls();

    this.perfilService.getMiPerfil().subscribe({
      next: (data) => {
        this.perfil.set(data);
        this.fotoUrl.set(data.foto_perfil ?? null);

        this.form.patchValue({
          telefono_personal: data.telefono_personal ?? '',
          correo_personal: data.correo_personal ?? '',
          grado_academico: data.grado_academico ?? '',
          especialidades: data.especialidades ?? '',
          experiencia: data.experiencia ?? '',
          domicilio_calle: data.domicilio_calle ?? '',
          domicilio_colonia: data.domicilio_colonia ?? '',
          domicilio_cp: data.domicilio_cp ?? '',
          domicilio_municipio: data.domicilio_municipio ?? '',
          domicilio_estado: data.domicilio_estado ?? '',
        });

        // 🔐 Si el backend te da una URL protegida para cv_archivo:
        // la descargamos como Blob con token (interceptor) y la montamos como blob: para el visor
        if (data.cv_archivo) {
          this.cargarPdfProtegidoEnVisor(data.cv_archivo, 'curriculum.pdf');
        }

        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
        this.mostrarToastError('No se pudo cargar tu perfil.');
      },
    });
  }

  // ================================
  // FOTO
  // ================================
  onFotoChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      this.mostrarToastError('Solo se permiten imágenes');
      return;
    }

    this.fotoFile = file;

    const reader = new FileReader();
    reader.onload = () => this.fotoUrl.set(reader.result as string);
    reader.readAsDataURL(file);

    this.dirtyState.set(true);
    this.generarAlertas();
  }

  // ================================
  // CV (PDF) -> visor propio (blob)
  // ================================
  onCvChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
      this.mostrarToastError('El currículum debe ser un PDF');
      return;
    }

    this.cvFile = file;
    this.cvNombre.set(file.name || 'curriculum.pdf');

    // reemplazar visor
    this.setSinglePdfViewerFromBlob(file);

    this.dirtyState.set(true);
    this.generarAlertas();
  }

  private setSinglePdfViewerFromBlob(file: File) {
    // revocar anterior (cv)
    const prev = this.cvRawUrl();
    if (prev) this.revokeObjectUrl(prev);

    const raw = URL.createObjectURL(file);
    this.trackObjectUrl(raw);

    this.cvRawUrl.set(raw);
    this.cvSafeUrl.set(this.sanitizer.bypassSecurityTrustResourceUrl(raw));
  }

  // ================================
  // DOCUMENTOS EXTRA (PDF/IMG) -> previews blob
  // ================================
  onDocsChange(event: Event) {
    const files = Array.from((event.target as HTMLInputElement).files ?? []);
    if (!files.length) return;

    const invalid = files.find((f) => !(f.type === 'application/pdf' || f.type.startsWith('image/')));
    if (invalid) {
      this.mostrarToastError('Solo se permiten PDF o imágenes en documentos extra');
      return;
    }

    // 🧼 revocar previews anteriores de docs
    this.clearDocsPreviews();

    this.documentosExtras = files;

    const previews: DocPreview[] = files.map((file) => {
      const raw = URL.createObjectURL(file);
      this.trackObjectUrl(raw);

      return {
        name: file.name,
        type: file.type,
        rawUrl: raw,
        safeUrl: this.sanitizer.bypassSecurityTrustResourceUrl(raw),
      };
    });

    this.docsPreviews.set(previews);
    this.dirtyState.set(true);
    this.generarAlertas();
  }

  // ================================
  // 🔐 CARGAR PDF REMOTO PROTEGIDO (TOKEN) Y MOSTRAR EN VISOR
  // ================================
  private cargarPdfProtegidoEnVisor(url: string, filename: string) {
    // revocar anterior (cv)
    const prev = this.cvRawUrl();
    if (prev) this.revokeObjectUrl(prev);

    this.cvSafeUrl.set(null);
    this.cvRawUrl.set(null);
    this.cvNombre.set(filename);

    this.archivosService
      .descargarComoBlob(url) // token via interceptor (recomendado)
      .pipe(finalize(() => {}))
      .subscribe({
        next: (blob) => {
          const raw = URL.createObjectURL(blob);
          this.trackObjectUrl(raw);

          this.cvRawUrl.set(raw);
          this.cvSafeUrl.set(this.sanitizer.bypassSecurityTrustResourceUrl(raw));
        },
        error: () => {
          this.mostrarToastError('No se pudo cargar el PDF protegido.');
        },
      });
  }

  // ================================
  // ACCIONES VISOR (abrir/descargar)
  // ================================
  abrirCvEnOtraPestana() {
    const raw = this.cvRawUrl();
    if (!raw) return;
    window.open(raw, '_blank', 'noopener');
  }

  descargarCv() {
    const raw = this.cvRawUrl();
    if (!raw) return;
    this.descargarDesdeObjectUrl(raw, this.cvNombre());
  }

  abrirDocEnOtraPestana(rawUrl: string) {
    window.open(rawUrl, '_blank', 'noopener');
  }

  descargarDoc(rawUrl: string, name: string) {
    this.descargarDesdeObjectUrl(rawUrl, name);
  }

  private descargarDesdeObjectUrl(rawUrl: string, filename: string) {
    const a = document.createElement('a');
    a.href = rawUrl;
    a.download = filename || 'archivo';
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  // ================================
  // ALERTAS
  // ================================
  private generarAlertas() {
    const alerts: string[] = [];
    const p = this.perfil();
    if (!p) {
      this.alertas.set([]);
      return;
    }

    if (!p.foto_perfil && !this.fotoFile) alerts.push('Falta subir foto de perfil.');
    if (!p.cv_archivo && !this.cvFile && !this.cvRawUrl()) alerts.push('Falta subir currículum (PDF).');
    if (!this.form.value.experiencia && !p.experiencia) alerts.push('Completa tu experiencia profesional.');

    this.alertas.set(alerts);
  }

  // ================================
  // GUARDAR (modal)
  // ================================
  intentarGuardar() {
    const emailControl = this.form.get('correo_personal');
    if (emailControl?.value && emailControl.invalid) {
      this.mostrarToastError('El correo electrónico no es válido.');
      return;
    }
    this.mostrarModalConfirmar.set(true);
  }

  confirmarGuardado() {
    this.mostrarModalConfirmar.set(false);
    this.guardarPerfil();
  }

  cancelarGuardado() {
    this.mostrarModalConfirmar.set(false);
  }

  guardarPerfil() {
    const fd = new FormData();

    Object.entries(this.form.value).forEach(([key, value]) => {
      fd.append(key, (value ?? '').toString());
    });

    if (this.fotoFile) fd.append('foto_perfil', this.fotoFile);
    if (this.cvFile) fd.append('cv_archivo', this.cvFile);

    this.documentosExtras.forEach((doc, index) => {
      fd.append(`documentos_extra_${index}`, doc);
    });

    this.guardando.set(true);

    this.perfilService.actualizarMiPerfil(fd).subscribe({
      next: (perfilActualizado) => {
        this.perfil.set(perfilActualizado);
        this.guardando.set(false);
        this.dirtyState.set(false);
        this.mostrarToastExito('Perfil actualizado correctamente');

        // 🧼 al guardar, si backend devuelve nueva URL protegida, recárgala como blob
        if (perfilActualizado.cv_archivo) {
          this.cargarPdfProtegidoEnVisor(perfilActualizado.cv_archivo, 'curriculum.pdf');
        }

        this.generarAlertas();
      },
      error: () => {
        this.guardando.set(false);
        this.mostrarToastError('Error al guardar los cambios');
      },
    });
  }

  // ================================
  // PASSWORD
  // ================================
  abrirCambioPassword() {
    this.passwordActual = '';
    this.passwordNueva = '';
    this.passwordConfirmar = '';
    this.mostrarModalPassword.set(true);
  }

  cerrarModalPassword() {
    this.mostrarModalPassword.set(false);
  }

  cambiarPassword() {
    if (!this.passwordActual || !this.passwordNueva || !this.passwordConfirmar) {
      this.mostrarToastError('Completa todos los campos de contraseña');
      return;
    }
    if (this.passwordNueva !== this.passwordConfirmar) {
      this.mostrarToastError('Las contraseñas nuevas no coinciden');
      return;
    }
    if (this.passwordNueva.length < 8) {
      this.mostrarToastError('La contraseña debe tener al menos 8 caracteres');
      return;
    }

    // TODO: conectar servicio real
    this.mostrarToastExito('Contraseña actualizada correctamente');
    this.cerrarModalPassword();
  }

  // ================================
  // TOAST
  // ================================
  private mostrarToastExito(mensaje: string) {
    this.toastTipo.set('success');
    this.toastMensaje.set(mensaje);
    this.mostrarToast.set(true);
    setTimeout(() => this.mostrarToast.set(false), 3500);
  }

  private mostrarToastError(mensaje: string) {
    this.toastTipo.set('error');
    this.toastMensaje.set(mensaje);
    this.mostrarToast.set(true);
    setTimeout(() => this.mostrarToast.set(false), 4000);
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

  // ================================
  // 🧼 LIMPIEZA / URLS
  // ================================
  private trackObjectUrl(rawUrl: string) {
    this.allocatedObjectUrls.add(rawUrl);
  }

  private revokeObjectUrl(rawUrl: string) {
    try {
      URL.revokeObjectURL(rawUrl);
    } catch {}
    this.allocatedObjectUrls.delete(rawUrl);
  }

  private clearDocsPreviews() {
    const prevDocs = this.docsPreviews();
    prevDocs.forEach((d) => this.revokeObjectUrl(d.rawUrl));
    this.docsPreviews.set([]);
  }

  private resetVisoresYUrls() {
    // CV
    const prevCv = this.cvRawUrl();
    if (prevCv) this.revokeObjectUrl(prevCv);

    this.cvSafeUrl.set(null);
    this.cvRawUrl.set(null);

    // Docs
    this.clearDocsPreviews();

    // Por si quedó algo suelto:
    this.allocatedObjectUrls.forEach((u) => this.revokeObjectUrl(u));
    this.allocatedObjectUrls.clear();
  }

  ngOnDestroy(): void {
    this.resetVisoresYUrls();
  }
}
