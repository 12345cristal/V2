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
import {
  DomSanitizer,
  SafeResourceUrl,
} from '@angular/platform-browser';
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
  // STATE
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

  // ================================
  // ARCHIVOS
  // ================================
  fotoFile: File | null = null;
  cvFile: File | null = null;
  documentosExtras: File[] = [];

  cvSafeUrl = signal<SafeResourceUrl | null>(null);
  cvRawUrl = signal<string | null>(null);
  cvNombre = signal('curriculum.pdf');

  docsPreviews = signal<DocPreview[]>([]);

  private allocatedObjectUrls = new Set<string>();

  // ================================
  // FORM
  // ================================
  form = this.fb.group({
    telefono_personal: [''],
    correo_personal: ['', Validators.email],
    grado_academico: [''],
    especialidades: [''],
    experiencia: [''],
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
        this.form.patchValue(data);

        // ✅ FOTO (BLOB PROTEGIDO)
        if (data.foto_perfil) {
          this.archivosService
            .descargarComoBlob(data.foto_perfil)
            .subscribe((blob) => {
              const raw = URL.createObjectURL(blob);
              this.trackObjectUrl(raw);
              this.fotoUrl.set(raw);
            });
        }

        // ✅ CV (PDF PROTEGIDO)
        if (data.cv_archivo) {
          this.cargarPdfProtegidoEnVisor(
            data.cv_archivo,
            'curriculum.pdf'
          );
        }

        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
        this.mostrarToastError(
          'No se pudo cargar tu perfil.'
        );
      },
    });
  }

  // ================================
  // FOTO
  // ================================
  onFotoChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file || !file.type.startsWith('image/')) {
      this.mostrarToastError('Solo imágenes');
      return;
    }

    this.fotoFile = file;
    const raw = URL.createObjectURL(file);
    this.trackObjectUrl(raw);
    this.fotoUrl.set(raw);
    this.dirtyState.set(true);
  }

  // ================================
  // CV
  // ================================
  onCvChange(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file || file.type !== 'application/pdf') {
      this.mostrarToastError('Solo PDF');
      return;
    }

    this.cvFile = file;
    this.cvNombre.set(file.name);
    this.setSinglePdfViewerFromBlob(file);
    this.dirtyState.set(true);
  }

  private setSinglePdfViewerFromBlob(file: File) {
    const currentUrl = this.cvRawUrl();
    if (currentUrl) this.revokeObjectUrl(currentUrl);

    const raw = URL.createObjectURL(file);
    this.trackObjectUrl(raw);

    this.cvRawUrl.set(raw);
    this.cvSafeUrl.set(
      this.sanitizer.bypassSecurityTrustResourceUrl(raw)
    );
  }

  private cargarPdfProtegidoEnVisor(
    url: string,
    filename: string
  ) {
    this.archivosService
      .descargarComoBlob(url)
      .pipe(finalize(() => {}))
      .subscribe({
        next: (blob) => {
          const raw = URL.createObjectURL(blob);
          this.trackObjectUrl(raw);
          this.cvRawUrl.set(raw);
          this.cvSafeUrl.set(
            this.sanitizer.bypassSecurityTrustResourceUrl(raw)
          );
          this.cvNombre.set(filename);
        },
        error: () =>
          this.mostrarToastError(
            'No se pudo cargar el PDF'
          ),
      });
  }

  // ================================
  // DOCUMENTOS EXTRA
  // ================================
  onDocsChange(event: Event) {
    const files = Array.from(
      (event.target as HTMLInputElement).files ?? []
    );
    if (!files.length) return;

    const invalid = files.find(
      (f) =>
        !(
          f.type === 'application/pdf' ||
          f.type.startsWith('image/')
        )
    );
    if (invalid) {
      this.mostrarToastError(
        'Solo se permiten PDF o imágenes en documentos extra'
      );
      return;
    }

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

  private clearDocsPreviews() {
    const prevDocs = this.docsPreviews();
    prevDocs.forEach((d) => this.revokeObjectUrl(d.rawUrl));
    this.docsPreviews.set([]);
  }

  abrirDocEnOtraPestana(rawUrl: string) {
    window.open(rawUrl, '_blank', 'noopener');
  }

  // ================================
  // GUARDAR
  // ================================
  guardarPerfil() {
    const fd = new FormData();

    Object.entries(this.form.value).forEach(([k, v]) =>
      fd.append(k, (v ?? '').toString())
    );

    if (this.fotoFile) fd.append('foto_perfil', this.fotoFile);
    if (this.cvFile) fd.append('cv_archivo', this.cvFile);

    // Agregar documentos extras
    this.documentosExtras.forEach((doc, idx) => {
      fd.append(`documentos_extras`, doc);
    });

    this.guardando.set(true);

    this.perfilService.actualizarMiPerfil(fd).subscribe({
      next: () => {
        this.guardando.set(false);
        this.dirtyState.set(false);
        this.mostrarToastExito(
          'Perfil actualizado correctamente'
        );
        this.cargarPerfil();
      },
      error: () => {
        this.guardando.set(false);
        this.mostrarToastError('Error al guardar');
      },
    });
  }

  // ================================
  // UTILIDADES
  // ================================
  private trackObjectUrl(url: string) {
    this.allocatedObjectUrls.add(url);
  }

  private revokeObjectUrl(url: string) {
    URL.revokeObjectURL(url);
    this.allocatedObjectUrls.delete(url);
  }

  private resetVisoresYUrls() {
    this.clearDocsPreviews();
    this.allocatedObjectUrls.forEach((u) =>
      URL.revokeObjectURL(u)
    );
    this.allocatedObjectUrls.clear();
  }

  private generarAlertas() {}

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

  @HostListener('window:beforeunload', ['$event'])
  onBeforeUnload(e: BeforeUnloadEvent) {
    if (this.dirtyState()) {
      e.preventDefault();
      e.returnValue = true;
    }
  }

  ngOnDestroy() {
    this.resetVisoresYUrls();
  }
}
