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
import {
  FormBuilder,
  ReactiveFormsModule,
  Validators,
  FormsModule,
} from '@angular/forms';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { finalize } from 'rxjs/operators';

import { PerfilService } from '../../service/perfil.service';
import { PerfilUsuario } from '../../interfaces/perfil-usuario.interface';
import { ArchivosService } from '../../service/archivos.service';
import { PdfViewerComponent } from './pdf-viewer.component';

type ToastTipo = 'success' | 'error';

type DocPreview = {
  name: string;
  type: string;
  rawUrl: string;
  safeUrl: SafeResourceUrl;
};

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
  // ARCHIVOS
  // ================================
  fotoFile: File | null = null;
  cvFile: File | null = null;
  documentosExtras: File[] = [];

  // ================================
  // VISOR PDF
  // ================================
  cvSafeUrl = signal<SafeResourceUrl | null>(null);
  cvRawUrl = signal<string | null>(null);
  cvNombre = signal('curriculum.pdf');

  docsPreviews = signal<DocPreview[]>([]);
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
  // CARGAR PERFIL
  // ================================
  cargarPerfil() {
    this.cargando.set(true);
    this.resetVisoresYUrls();

    this.perfilService.getMiPerfil().subscribe({
      next: (data) => {
        this.perfil.set(data);

        this.form.patchValue(data as any);

        if (data.foto_perfil) {
          this.archivosService.descargarComoBlob(data.foto_perfil).subscribe({
            next: (blob) => {
              const raw = URL.createObjectURL(blob);
              this.trackObjectUrl(raw);
              this.fotoUrl.set(raw);
            },
          });
        }

        if (data.cv_archivo) {
          this.cargarPdfProtegidoEnVisor(data.cv_archivo, 'curriculum.pdf');
        }

        if (data.documentos_extra && data.documentos_extra.length > 0) {
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

  private cargarDocumentosExtra(urls: string[]) {
    const previews: DocPreview[] = [];
    
    urls.forEach((url) => {
      this.archivosService.descargarComoBlob(url).subscribe({
        next: (blob) => {
          const raw = URL.createObjectURL(blob);
          this.trackObjectUrl(raw);
          const filename = url.split('/').pop() || 'archivo';
          const type = blob.type;
          
          previews.push({
            name: filename,
            type: type,
            rawUrl: raw,
            safeUrl: this.sanitizer.bypassSecurityTrustResourceUrl(raw),
          });
          
          if (previews.length === urls.length) {
            this.docsPreviews.set(previews);
          }
        },
      });
    });
  }

  // ================================
  // FOTO
  // ================================
  onFotoChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file || !file.type.startsWith('image/')) return;

    this.fotoFile = file;

    const raw = URL.createObjectURL(file);
    this.trackObjectUrl(raw);
    this.fotoUrl.set(raw);

    this.dirtyState.set(true);
    this.generarAlertas();
  }

  // ================================
  // CV
  // ================================
  onCvChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file || file.type !== 'application/pdf') return;

    this.cvFile = file;
    this.cvNombre.set(file.name);
    this.setPdfFromBlob(file);

    this.dirtyState.set(true);
    this.generarAlertas();
  }

  private setPdfFromBlob(file: File) {
    const prev = this.cvRawUrl();
    if (prev) this.revokeObjectUrl(prev);

    const raw = URL.createObjectURL(file);
    this.trackObjectUrl(raw);
    this.cvRawUrl.set(raw);
    this.cvSafeUrl.set(this.sanitizer.bypassSecurityTrustResourceUrl(raw));
  }

  // ================================
  // DOCUMENTOS EXTRA
  // ================================
  onDocsChange(event: Event) {
    const files = Array.from((event.target as HTMLInputElement).files ?? []);
    if (!files.length) return;

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
  }

  // ================================
  // VISOR REMOTO PDF
  // ================================
  private cargarPdfProtegidoEnVisor(url: string, name: string) {
    this.archivosService.descargarComoBlob(url).subscribe({
      next: (blob) => {
        const raw = URL.createObjectURL(blob);
        this.trackObjectUrl(raw);
        this.cvRawUrl.set(raw);
        this.cvSafeUrl.set(this.sanitizer.bypassSecurityTrustResourceUrl(raw));
        this.cvNombre.set(name);
      },
    });
  }

  // ================================
  // ACCIONES
  // ================================
  abrirCvEnOtraPestana() {
    if (this.cvRawUrl()) window.open(this.cvRawUrl()!, '_blank');
  }

  descargarCv() {
    if (this.cvRawUrl()) this.descargarDesdeUrl(this.cvRawUrl()!, this.cvNombre());
  }

  abrirDocEnOtraPestana(raw: string) {
    window.open(raw, '_blank');
  }

  descargarDoc(raw: string, name: string) {
    this.descargarDesdeUrl(raw, name);
  }

  private descargarDesdeUrl(raw: string, name: string) {
    const a = document.createElement('a');
    a.href = raw;
    a.download = name;
    a.click();
  }

  // ================================
  // GUARDAR
  // ================================
  intentarGuardar() {
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

    Object.entries(this.form.value).forEach(([k, v]) =>
      fd.append(k, v?.toString() ?? '')
    );

    if (this.fotoFile) fd.append('foto_perfil', this.fotoFile);
    if (this.cvFile) fd.append('cv_archivo', this.cvFile);
    this.documentosExtras.forEach((d, i) =>
      fd.append(`documentos_extra_${i}`, d)
    );

    this.guardando.set(true);

    this.perfilService.actualizarMiPerfil(fd).subscribe({
      next: (p) => {
        this.perfil.set(p);
        this.guardando.set(false);
        this.dirtyState.set(false);
        this.mostrarToastExito('Perfil actualizado correctamente');
      },
      error: () => {
        this.guardando.set(false);
        this.mostrarToastError('Error al guardar');
      },
    });
  }

  // ================================
  // PASSWORD
  // ================================
  abrirCambioPassword() {
    this.mostrarModalPassword.set(true);
  }

  cerrarModalPassword() {
    this.mostrarModalPassword.set(false);
  }

  cambiarPassword() {
    this.mostrarToastExito('Contraseña actualizada');
    this.cerrarModalPassword();
  }

  // ================================
  // TOAST
  // ================================
  private mostrarToastExito(msg: string) {
    this.toastTipo.set('success');
    this.toastMensaje.set(msg);
    this.mostrarToast.set(true);
    setTimeout(() => this.mostrarToast.set(false), 3000);
  }

  private mostrarToastError(msg: string) {
    this.toastTipo.set('error');
    this.toastMensaje.set(msg);
    this.mostrarToast.set(true);
    setTimeout(() => this.mostrarToast.set(false), 4000);
  }

  // ================================
  // ALERTAS
  // ================================
  private generarAlertas() {
    const a: string[] = [];
    const p = this.perfil();
    if (!p) return;

    if (!p.foto_perfil && !this.fotoFile) a.push('Falta subir foto de perfil');
    if (!p.cv_archivo && !this.cvFile) a.push('Falta subir currículum');

    this.alertas.set(a);
  }

  // ================================
  // LIMPIEZA
  // ================================
  private trackObjectUrl(u: string) {
    this.allocatedObjectUrls.add(u);
  }

  private revokeObjectUrl(u: string) {
    try {
      URL.revokeObjectURL(u);
    } catch {}
    this.allocatedObjectUrls.delete(u);
  }

  private clearDocsPreviews() {
    this.docsPreviews().forEach((d) => this.revokeObjectUrl(d.rawUrl));
    this.docsPreviews.set([]);
  }

  private resetVisoresYUrls() {
    if (this.cvRawUrl()) this.revokeObjectUrl(this.cvRawUrl()!);
    this.cvRawUrl.set(null);
    this.cvSafeUrl.set(null);
    this.clearDocsPreviews();
  }

  ngOnDestroy(): void {
    this.resetVisoresYUrls();
  }

  @HostListener('window:beforeunload', ['$event'])
  onBeforeUnload(e: BeforeUnloadEvent) {
    if (this.dirtyState()) {
      e.preventDefault();
      e.returnValue = true;
    }
  }
}
