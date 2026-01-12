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
import { environment } from '../../enviroment/environment';

import { PerfilService } from '../../service/perfil.service';
import { PerfilUsuario } from '../../interfaces/perfil-usuario.interface';
import { PdfViewerComponent } from './pdf-viewer.component';

type ToastTipo = 'success' | 'error';

interface DocPreview {
  name: string;
  type: string;
  rawUrl: string;
  safeUrl: SafeResourceUrl;
}

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
  // ============================
  // INYECCIONES
  // ============================
  private fb = inject(FormBuilder);
  private injector = inject(Injector);
  private perfilService = inject(PerfilService);
  private sanitizer = inject(DomSanitizer);
  private destroyRef = inject(DestroyRef);

  // ============================
  // SIGNALS - ESTADO GENERAL
  // ============================
  perfil = signal<PerfilUsuario | null>(null);
  cargando = signal(true);
  guardando = signal(false);
  dirtyState = signal(false);
  alertas = signal<string[]>([]);

  // ============================
  // SIGNALS - NOTIFICACIONES
  // ============================
  mostrarToast = signal(false);
  toastTipo = signal<ToastTipo>('success');
  toastMensaje = signal('');

  // ============================
  // SIGNALS - MODALES
  // ============================
  mostrarModalConfirmar = signal(false);
  mostrarModalPassword = signal(false);

  // ============================
  // ARCHIVOS - REFERENCIAS
  // ============================
  fotoFile: File | null = null;
  cvFile: File | null = null;
  documentosExtras: File[] = [];

  // ============================
  // SIGNALS - PREVISUALIZACIONES
  // ============================
  fotoUrl = signal<string | null>(null);
  cvSafeUrl = signal<SafeResourceUrl | null>(null);
  cvRawUrl = signal<string | null>(null);
  cvNombre = signal('curriculum.pdf');
  docsPreview = signal<DocPreview[]>([]);

  // ============================
  // CONTROL DE URLS (para limpiar)
  // ============================
  private allocatedObjectUrls = new Set<string>();

  // ============================
  // PASSWORD
  // ============================
  passwordActual = '';
  passwordNueva = '';
  passwordConfirmar = '';

  // ============================
  // FORM
  // ============================
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

  // ============================
  // CARGAR PERFIL (API)
  // ============================
  cargarPerfil(): void {
    this.cargando.set(true);
    this.resetVisoresYUrls();

    this.perfilService.getMiPerfil().subscribe({
      next: (data) => {
        this.perfil.set(data);
        this.form.patchValue(data as any);

        // Cargar foto
        if (data.foto_perfil) {
          this.cargarFoto(data.foto_perfil);
        }

        // Cargar CV
        if (data.cv_archivo) {
          this.cargarCV(data.cv_archivo);
        }

        // Cargar documentos extra
        if (data.documentos_extra && Array.isArray(data.documentos_extra)) {
          this.cargarDocumentosExtra(data.documentos_extra);
        }

        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
        this.mostrarToastError('No se pudo cargar el perfil');
      },
    });
  }

  // ============================
  // CARGAR FOTO EXISTENTE
  // ============================
  private cargarFoto(rutaRelativa: string): void {
    const filename = rutaRelativa.split('/').pop() || rutaRelativa;
    const urlCompleta = `${environment.apiBaseUrl}/perfil/archivos/fotos/${filename}`;
    
    this.perfilService.descargarArchivoProtegido(urlCompleta).subscribe({
      next: (blob) => {
        const blobUrl = URL.createObjectURL(blob);
        this.allocatedObjectUrls.add(blobUrl);
        this.fotoUrl.set(blobUrl);
      },
    });
  }

  // ============================
  // CARGAR CV EXISTENTE CON BLOB
  // ============================
  private cargarCV(rutaRelativa: string): void {
    const filename = rutaRelativa.split('/').pop() || 'curriculum.pdf';
    const urlCompleta = `${environment.apiBaseUrl}/perfil/archivos/cv/${filename}`;
    
    this.perfilService.descargarArchivoProtegido(urlCompleta).subscribe({
      next: (blob) => {
        const blobUrl = URL.createObjectURL(blob);
        this.allocatedObjectUrls.add(blobUrl);
        
        const safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
          `${blobUrl}#toolbar=0`
        );
        this.cvSafeUrl.set(safeUrl);
        this.cvRawUrl.set(blobUrl);
        this.cvNombre.set(filename);
      },
    });
  }

  // ============================
  // CARGAR DOCUMENTOS EXTRA
  // ============================
  private cargarDocumentosExtra(rutas: string[]): void {
    const previews: DocPreview[] = [];
    let processados = 0;

    rutas.forEach((rutaRelativa) => {
      const filename = rutaRelativa.split('/').pop() || 'documento';
      const urlCompleta = `${environment.apiBaseUrl}/perfil/archivos/documentos/${filename}`;

      // Descargar con blob (protegido con JWT)
      this.perfilService.descargarArchivoProtegido(urlCompleta).subscribe({
        next: (blob) => {
          const blobUrl = URL.createObjectURL(blob);
          this.allocatedObjectUrls.add(blobUrl);
          
          const isSafePdf = blob.type === 'application/pdf';
          const safeUrl = isSafePdf
            ? this.sanitizer.bypassSecurityTrustResourceUrl(`${blobUrl}#toolbar=0`)
            : this.sanitizer.bypassSecurityTrustResourceUrl(blobUrl);
          
          previews.push({
            name: filename,
            type: blob.type,
            rawUrl: blobUrl,
            safeUrl,
          });
          
          processados++;
          if (processados === rutas.length) {
            this.docsPreview.set(previews);
          }
        },
      });
    });
  }

  // ============================
  // HANDLERS - CAMBIOS DE ARCHIVOS
  // ============================
  onFotoChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (!file) return;

    // Validar tipo
    if (!file.type.startsWith('image/')) {
      this.mostrarToastError('La foto debe ser una imagen (JPG, PNG, etc)');
      return;
    }

    // Validar tamaño (máximo 5MB)
    if (file.size > 5 * 1024 * 1024) {
      this.mostrarToastError('La foto no puede superar 5MB');
      return;
    }

    this.fotoFile = file;
    this.dirtyState.set(true);

    // Previsualizar
    const reader = new FileReader();
    reader.onload = () => {
      const blobUrl = reader.result as string;
      this.fotoUrl.set(blobUrl);
    };
    reader.readAsDataURL(file);
  }

  onCvChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (!file) return;

    // Validar tipo
    if (file.type !== 'application/pdf') {
      this.mostrarToastError('El CV debe ser un PDF');
      return;
    }

    // Validar tamaño (máximo 10MB)
    if (file.size > 10 * 1024 * 1024) {
      this.mostrarToastError('El CV no puede superar 10MB');
      return;
    }

    this.cvFile = file;
    this.dirtyState.set(true);
    this.cvNombre.set(file.name);

    // Previsualizar
    const reader = new FileReader();
    reader.onload = () => {
      const blobUrl = reader.result as string;
      const safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(
        `${blobUrl}#toolbar=0`
      );
      this.cvSafeUrl.set(safeUrl);
    };
    reader.readAsDataURL(file);
  }

  onDocsChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    const files = Array.from(input.files || []);

    if (files.length === 0) return;

    // Validar cada archivo
    const validos: File[] = [];
    for (const file of files) {
      const esPdf = file.type === 'application/pdf';
      const esImagen = file.type.startsWith('image/');
      const tamañoOk = file.size <= 10 * 1024 * 1024; // 10MB

      if (!esPdf && !esImagen) {
        this.mostrarToastError(`${file.name} no es un PDF o imagen`);
        continue;
      }

      if (!tamañoOk) {
        this.mostrarToastError(`${file.name} supera 10MB`);
        continue;
      }

      validos.push(file);
    }

    this.documentosExtras = validos;
    this.dirtyState.set(true);

    // Previsualizar
    const previews: DocPreview[] = [];
    validos.forEach((file) => {
      const reader = new FileReader();
      reader.onload = () => {
        const blobUrl = reader.result as string;
        const isSafePdf = file.type === 'application/pdf';
        const safeUrl = isSafePdf
          ? this.sanitizer.bypassSecurityTrustResourceUrl(
              `${blobUrl}#toolbar=0`
            )
          : this.sanitizer.bypassSecurityTrustUrl(blobUrl);

        previews.push({
          name: file.name,
          type: file.type,
          rawUrl: blobUrl,
          safeUrl,
        });
        this.docsPreview.set([...previews]);
      };
      reader.readAsDataURL(file);
    });
  }

  // ============================
  // GUARDAR PERFIL
  // ============================
  intentarGuardar(): void {
    if (!this.form.valid) {
      this.mostrarToastError('Completa los campos correctamente');
      return;
    }
    this.mostrarModalConfirmar.set(true);
  }

  confirmarGuardar(): void {
    this.mostrarModalConfirmar.set(false);
    this.guardarPerfil();
  }

  cancelarGuardado(): void {
    this.mostrarModalConfirmar.set(false);
  }

  // ============================
  // ACCIONES DE ARCHIVOS
  // ============================
  abrirCvEnOtraPestana(): void {
    if (this.cvRawUrl()) {
      window.open(this.cvRawUrl()!, '_blank');
    }
  }

  descargarCv(): void {
    if (this.cvRawUrl() && this.cvRawUrl()?.startsWith('http')) {
      const a = document.createElement('a');
      a.href = this.cvRawUrl()!;
      a.download = this.cvNombre();
      a.click();
    }
  }

  abrirDocEnOtraPestana(rawUrl: string): void {
    if (rawUrl.startsWith('http')) {
      window.open(rawUrl, '_blank');
    }
  }

  descargarDoc(rawUrl: string, name: string): void {
    if (rawUrl.startsWith('http')) {
      const a = document.createElement('a');
      a.href = rawUrl;
      a.download = name;
      a.click();
    }
  }

  private guardarPerfil(): void {
    this.guardando.set(true);

    const formData = new FormData();

    // Agregar campos del formulario
    const values = this.form.getRawValue();
    Object.entries(values).forEach(([key, value]) => {
      if (value) formData.append(key, value as string);
    });

    // Agregar archivos nuevos
    if (this.fotoFile) {
      formData.append('foto_perfil', this.fotoFile);
    }
    if (this.cvFile) {
      formData.append('cv_archivo', this.cvFile);
    }
    if (this.documentosExtras.length > 0) {
      this.documentosExtras.forEach((file, i) => {
        formData.append(`documentos_extra_${i}`, file);
      });
    }

    this.perfilService
      .actualizarMiPerfil(formData)
      .pipe(finalize(() => this.guardando.set(false)))
      .subscribe({
        next: (data) => {
          this.perfil.set(data);
          this.fotoFile = null;
          this.cvFile = null;
          this.documentosExtras = [];
          this.dirtyState.set(false);
          this.mostrarToastExito('Perfil actualizado correctamente');
          this.cargarPerfil();
        },
        error: (err) => {
          this.mostrarToastError(
            err?.error?.detail || 'Error al guardar el perfil'
          );
        },
      });
  }

  // ============================
  // PASSWORD
  // ============================
  abrirCambioPassword(): void {
    this.mostrarModalPassword.set(true);
  }

  cerrarModalPassword(): void {
    this.mostrarModalPassword.set(false);
  }

  cambiarPassword(): void {
    this.mostrarToastExito('Contraseña actualizada');
    this.cerrarModalPassword();
  }

  // ============================
  // NOTIFICACIONES (TOAST)
  // ============================
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

  // ============================
  // ============================
  // ALERTAS
  // ============================
  private generarAlertas(): void {
    const a: string[] = [];
    const p = this.perfil();
    if (!p) return;

    if (!p.foto_perfil && !this.fotoFile) a.push('Falta subir foto de perfil');
    if (!p.cv_archivo && !this.cvFile) a.push('Falta subir currículum');

    this.alertas.set(a);
  }

  // ============================
  // LIMPIEZA
  // ============================
  private resetVisoresYUrls(): void {
    // Solo revocar URLs de blob locales
    if (this.cvRawUrl() && this.cvRawUrl()?.startsWith('blob:')) {
      URL.revokeObjectURL(this.cvRawUrl()!);
      this.allocatedObjectUrls.delete(this.cvRawUrl()!);
    }
    this.cvRawUrl.set(null);
    this.cvSafeUrl.set(null);
    
    // Limpiar previews
    this.docsPreview().forEach((d) => {
      if (d.rawUrl.startsWith('blob:')) {
        URL.revokeObjectURL(d.rawUrl);
        this.allocatedObjectUrls.delete(d.rawUrl);
      }
    });
    this.docsPreview.set([]);
  }

  @HostListener('window:beforeunload', ['$event'])
  onBeforeUnload(e: BeforeUnloadEvent): void {
    if (this.dirtyState()) {
      e.preventDefault();
      e.returnValue = true;
    }
  }
}
