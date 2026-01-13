import {
  Component,
  signal,
  effect,
  inject,
  Injector,
  runInInjectionContext,
  OnDestroy,
  DestroyRef,
  HostListener,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  ReactiveFormsModule,
  Validators,
  FormsModule,
} from '@angular/forms';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { finalize } from 'rxjs/operators';
import { environment } from '../../environment/environment';

import { PerfilService } from '../../service/perfil.service';
import { PerfilUsuario } from '../../interfaces/perfil-usuario.interface';
import { DocPreview } from '../../interfaces/DocPreview.interface';
import { PdfViewerComponent } from './pdf-viewer.component';

type ToastTipo = 'success' | 'error';

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    PdfViewerComponent,
  ],
  templateUrl: './perfil.html',
  styleUrls: ['./perfil.scss'],
})
export class PerfilComponent implements OnDestroy {
  // =====================================================
  // INYECCIONES
  // =====================================================
  private fb = inject(FormBuilder);
  private injector = inject(Injector);
  private perfilService = inject(PerfilService);
  private sanitizer = inject(DomSanitizer);
  private destroyRef = inject(DestroyRef);

  // =====================================================
  // ESTADO GENERAL
  // =====================================================
  perfil = signal<PerfilUsuario | null>(null);
  cargando = signal(true);
  guardando = signal(false);
  dirtyState = signal(false);
  alertas = signal<string[]>([]);

  // =====================================================
  // TOAST
  // =====================================================
  mostrarToast = signal(false);
  toastTipo = signal<ToastTipo>('success');
  toastMensaje = signal('');

  // =====================================================
  // MODALES
  // =====================================================
  mostrarModalConfirmar = signal(false);
  mostrarModalPassword = signal(false);

  // =====================================================
  // ARCHIVOS
  // =====================================================
  fotoFile: File | null = null;
  cvFile: File | null = null;
  documentosExtras: File[] = [];

  // =====================================================
  // PREVIEWS
  // =====================================================
  fotoUrl = signal<string | null>(null);                 // img
  cvSafeUrl = signal<SafeResourceUrl | null>(null);     // iframe
  cvRawUrl = signal<string | null>(null);               // blob:
  cvNombre = signal('curriculum.pdf');
  docsPreview = signal<DocPreview[]>([]);

  // =====================================================
  // CONTROL DE BLOB URLS
  // =====================================================
  private allocatedObjectUrls = new Set<string>();

  // =====================================================
  // PASSWORD
  // =====================================================
  passwordActual = '';
  passwordNueva = '';
  passwordConfirmar = '';

  // =====================================================
  // FORMULARIO
  // =====================================================
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

  ngOnDestroy(): void {
    this.allocatedObjectUrls.forEach(url => URL.revokeObjectURL(url));
    this.allocatedObjectUrls.clear();
  }

  // =====================================================
  // PERFIL
  // =====================================================
  cargarPerfil(): void {
    this.cargando.set(true);
    this.resetVisoresYUrls();

    this.perfilService.getMiPerfil().subscribe({
      next: (data) => {
        this.perfil.set(data);
        this.form.patchValue(data as any);
        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
        this.mostrarToastError('No se pudo cargar el perfil');
      },
    });
  }

  // =====================================================
  // FOTO
  // =====================================================
  cargarFotoOnDemand(): void {
    const p = this.perfil();
    if (!p?.foto_perfil || this.fotoUrl()) return;

    const filename = p.foto_perfil.split('/').pop()!;
    const url = `${environment.apiBaseUrl}/perfil/archivos/fotos/${filename}`;

    this.perfilService.descargarArchivoProtegido(url).subscribe(blob => {
      const blobUrl = URL.createObjectURL(blob);
      this.allocatedObjectUrls.add(blobUrl);
      this.fotoUrl.set(blobUrl); // IMG → URL normal
    });
  }

  onFotoChange(event: Event): void {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file || !file.type.startsWith('image/')) {
      this.mostrarToastError('La foto debe ser una imagen');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      this.mostrarToastError('La foto no puede superar 5MB');
      return;
    }

    this.fotoFile = file;
    this.dirtyState.set(true);

    const reader = new FileReader();
    reader.onload = () => this.fotoUrl.set(reader.result as string);
    reader.readAsDataURL(file);
  }

  // =====================================================
  // CV (PDF)
  // =====================================================
  private cargarCV(ruta: string, cb?: () => void): void {
    const filename = ruta.split('/').pop()!;
    const url = `${environment.apiBaseUrl}/perfil/archivos/cv/${filename}`;

    this.perfilService.descargarArchivoProtegido(url).subscribe(blob => {
      const blobUrl = URL.createObjectURL(blob);
      this.allocatedObjectUrls.add(blobUrl);

      this.cvSafeUrl.set(
        this.sanitizer.bypassSecurityTrustResourceUrl(
          `${blobUrl}#toolbar=0`
        )
      );
      this.cvRawUrl.set(blobUrl);
      this.cvNombre.set(filename);
      cb?.();
    });
  }

  onCvChange(event: Event): void {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file || file.type !== 'application/pdf') {
      this.mostrarToastError('El CV debe ser PDF');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      this.mostrarToastError('El CV no puede superar 10MB');
      return;
    }

    this.cvFile = file;
    this.cvNombre.set(file.name);
    this.dirtyState.set(true);

    const reader = new FileReader();
    reader.onload = () => {
      this.cvSafeUrl.set(
        this.sanitizer.bypassSecurityTrustResourceUrl(
          `${reader.result as string}#toolbar=0`
        )
      );
    };
    reader.readAsDataURL(file);
  }

  abrirCvEnOtraPestana(): void {
    const p = this.perfil();
    if (this.cvRawUrl()) {
      window.open(this.cvRawUrl()!, '_blank');
      return;
    }
    if (p?.cv_archivo) {
      this.cargarCV(p.cv_archivo, () => {
        window.open(this.cvRawUrl()!, '_blank');
      });
    }
  }

  descargarCv(): void {
    if (!this.cvRawUrl()) return;
    const a = document.createElement('a');
    a.href = this.cvRawUrl()!;
    a.download = this.cvNombre();
    a.click();
  }

  // =====================================================
  // DOCUMENTOS EXTRA
  // =====================================================
  cargarDocumentosExtra(rutas: string[]): void {
    const previews: DocPreview[] = [];
    let count = 0;

    rutas.forEach(ruta => {
      const filename = ruta.split('/').pop()!;
      const url = `${environment.apiBaseUrl}/perfil/archivos/documentos/${filename}`;

      this.perfilService.descargarArchivoProtegido(url).subscribe(blob => {
        const blobUrl = URL.createObjectURL(blob);
        this.allocatedObjectUrls.add(blobUrl);

        const isPdf = blob.type === 'application/pdf';
        const safeUrl = isPdf
          ? this.sanitizer.bypassSecurityTrustResourceUrl(`${blobUrl}#toolbar=0`)
          : this.sanitizer.bypassSecurityTrustUrl(blobUrl);

        previews.push({
          name: filename,
          type: blob.type,
          rawUrl: blobUrl,
          safeUrl,
          isPdf,
        });

        count++;
        if (count === rutas.length) {
          this.docsPreview.set(previews);
        }
      });
    });
  }

  onDocsChange(event: Event): void {
    const files = Array.from((event.target as HTMLInputElement).files || []);
    if (!files.length) return;

    this.documentosExtras = [];
    const previews: DocPreview[] = [];

    files.forEach(file => {
      const esPdf = file.type === 'application/pdf';
      const esImg = file.type.startsWith('image/');

      if (!esPdf && !esImg) return;

      this.documentosExtras.push(file);

      const reader = new FileReader();
      reader.onload = () => {
        const blobUrl = reader.result as string;
        previews.push({
          name: file.name,
          type: file.type,
          rawUrl: blobUrl,
          safeUrl: esPdf
            ? this.sanitizer.bypassSecurityTrustResourceUrl(`${blobUrl}#toolbar=0`)
            : this.sanitizer.bypassSecurityTrustUrl(blobUrl),
          isPdf: esPdf,
        });
        this.docsPreview.set([...previews]);
      };
      reader.readAsDataURL(file);
    });

    this.dirtyState.set(true);
  }

  // =====================================================
  // GUARDAR
  // =====================================================
  confirmarGuardar(): void {
    this.guardando.set(true);

    const fd = new FormData();
    Object.entries(this.form.getRawValue()).forEach(([k, v]) => {
      if (v) fd.append(k, v as string);
    });

    if (this.fotoFile) fd.append('foto_perfil', this.fotoFile);
    if (this.cvFile) fd.append('cv_archivo', this.cvFile);
    this.documentosExtras.forEach((f, i) =>
      fd.append(`documentos_extra_${i}`, f)
    );

    this.perfilService.actualizarMiPerfil(fd)
      .pipe(finalize(() => this.guardando.set(false)))
      .subscribe({
        next: () => {
          this.mostrarToastExito('Perfil actualizado correctamente');
          this.cargarPerfil();
        },
        error: () => this.mostrarToastError('Error al guardar perfil'),
      });
  }

  // =====================================================
  // UTILIDADES
  // =====================================================
  private generarAlertas(): void {
    const p = this.perfil();
    if (!p) return;

    const a: string[] = [];
    if (!p.foto_perfil) a.push('Falta foto de perfil');
    if (!p.cv_archivo) a.push('Falta currículum');
    this.alertas.set(a);
  }

  private resetVisoresYUrls(): void {
    this.allocatedObjectUrls.forEach(u => URL.revokeObjectURL(u));
    this.allocatedObjectUrls.clear();
    this.fotoUrl.set(null);
    this.cvSafeUrl.set(null);
    this.cvRawUrl.set(null);
    this.docsPreview.set([]);
  }

  private mostrarToastExito(msg: string): void {
    this.toastTipo.set('success');
    this.toastMensaje.set(msg);
    this.mostrarToast.set(true);
    setTimeout(() => this.mostrarToast.set(false), 3000);
  }

  private mostrarToastError(msg: string): void {
    this.toastTipo.set('error');
    this.toastMensaje.set(msg);
    this.mostrarToast.set(true);
    setTimeout(() => this.mostrarToast.set(false), 4000);
  }

  @HostListener('window:beforeunload', ['$event'])
  onBeforeUnload(e: BeforeUnloadEvent): void {
    if (this.dirtyState()) {
      e.preventDefault();
      e.returnValue = true;
    }
  }

  intentarGuardar(): void {
    this.mostrarModalConfirmar.set(true);
  }

  cancelarGuardado(): void {
    this.mostrarModalConfirmar.set(false);
  }

  abrirCambioPassword(): void {
    this.mostrarModalPassword.set(true);
  }

  cerrarModalPassword(): void {
    this.mostrarModalPassword.set(false);
    this.passwordActual = '';
    this.passwordNueva = '';
    this.passwordConfirmar = '';
  }

  cambiarPassword(): void {
    if (!this.passwordActual || !this.passwordNueva || !this.passwordConfirmar) {
      this.mostrarToastError('Todos los campos son obligatorios');
      return;
    }

    if (this.passwordNueva !== this.passwordConfirmar) {
      this.mostrarToastError('Las contraseñas no coinciden');
      return;
    }

    this.perfilService.cambiarPassword({
      password_actual: this.passwordActual,
      password_nueva: this.passwordNueva,
    }).subscribe({
      next: () => {
        this.mostrarToastExito('Contraseña cambiada exitosamente');
        this.cerrarModalPassword();
      },
      error: () => {
        this.mostrarToastError('Error al cambiar contraseña');
      },
    });
  }

  abrirDocEnOtraPestana(url: string): void {
    window.open(url, '_blank');
  }

  descargarDoc(url: string, nombre: string): void {
    const a = document.createElement('a');
    a.href = url;
    a.download = nombre;
    a.click();
  }
}
