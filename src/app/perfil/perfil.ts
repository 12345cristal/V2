import { Component, OnInit, OnDestroy, computed, signal, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { HttpClient } from '@angular/common/http';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { environment } from '../enviroment/environment';
import { PerfilUsuario } from '../interfaces/perfil-usuario.interface';

interface PreviewFile {
  file: File;
  preview: string;
  tipo: 'image' | 'pdf';
}

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatIconModule],
  templateUrl: './perfil.html',
  styleUrl: './perfil.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PerfilComponent implements OnInit, OnDestroy {
  private httpClient = inject(HttpClient);
  private fb = inject(FormBuilder);
  private sanitizer = inject(DomSanitizer);

  // ==================== SIGNALS ====================
  datosPersonales = signal<PerfilUsuario | null>(null);
  cargando = signal(false);
  guardando = signal(false);
  error = signal<string | null>(null);
  successMsg = signal<string | null>(null);
  
  tabActiva = signal<'datos' | 'documentos' | 'seguridad'>('datos');
  editandoDatos = signal(false);
  
  // Modal de confirmación
  mostrarModalConfirmacion = signal(false);
  archivoEnConfirmacion = signal<{ tipo: string; nombre: string; file: File } | null>(null);
  
  formDatos: FormGroup;
  
  // Archivos y previsualizaciones
  fotoPreview = signal<PreviewFile | null>(null);
  cvPreview = signal<PreviewFile | null>(null);
  documentosPreview = signal<PreviewFile[]>([]);
  
  // ObjectURLs para limpieza
  private objectUrls: string[] = [];
  
  // Flags de cambios
  hayCambios = computed(() => {
    return this.fotoPreview() !== null || 
           this.cvPreview() !== null || 
           this.documentosPreview().length > 0 ||
           this.formDatos.dirty;
  });

  // ==================== COMPUTED ====================
  documentosFaltantes = computed(() => {
    const datos = this.datosPersonales();
    if (!datos) return [];
    
    const faltantes: string[] = [];
    
    if (!datos.cv_archivo && !this.cvPreview()) {
      faltantes.push('Falta currículum vitae (CV)');
    }
    
    if (!datos.foto_perfil && !this.fotoPreview()) {
      faltantes.push('Falta foto de perfil');
    }
    
    return faltantes;
  });

  completitud = computed(() => {
    const datos = this.datosPersonales();
    if (!datos) return 0;
    
    let items = 0;
    let completados = 0;
    
    // Datos básicos
    items += 5;
    if (datos.nombres) completados++;
    if (datos.apellido_paterno) completados++;
    if (datos.telefono_personal) completados++;
    if (datos.correo_personal) completados++;
    if (datos.fecha_nacimiento) completados++;
    
    // Domicilio
    items += 3;
    if (datos.domicilio_calle) completados++;
    if (datos.domicilio_municipio) completados++;
    if (datos.domicilio_estado) completados++;
    
    // Profesional
    items += 2;
    if (datos.especialidades) completados++;
    if (datos.experiencia) completados++;
    
    // Documentos
    items += 2;
    if (datos.foto_perfil || this.fotoPreview()) completados++;
    if (datos.cv_archivo || this.cvPreview()) completados++;
    
    return Math.round((completados / items) * 100);
  });

  constructor() {
    this.formDatos = this.fb.group({
      telefono_personal: [''],
      correo_personal: ['', [Validators.email]],
      especialidades: [''],
      experiencia: [''],
      domicilio_calle: [''],
      domicilio_colonia: [''],
      domicilio_cp: [''],
      domicilio_municipio: [''],
      domicilio_estado: ['']
    });
  }

  ngOnInit() {
    this.cargarDatos();
  }

  ngOnDestroy() {
    this.limpiarObjectUrls();
  }

  // ==================== CARGAR DATOS ====================
  cargarDatos() {
    this.cargando.set(true);
    this.error.set(null);
    
    this.httpClient.get<PerfilUsuario>(`${environment.apiBaseUrl}/perfil/me`)
      .subscribe({
        next: async (datos) => {
          await this.cargarArchivos(datos);
          this.datosPersonales.set(datos);
          this.formDatos.patchValue({
            telefono_personal: datos.telefono_personal || '',
            correo_personal: datos.correo_personal || '',
            especialidades: datos.especialidades || '',
            experiencia: datos.experiencia || '',
            domicilio_calle: datos.domicilio_calle || '',
            domicilio_colonia: datos.domicilio_colonia || '',
            domicilio_cp: datos.domicilio_cp || '',
            domicilio_municipio: datos.domicilio_municipio || '',
            domicilio_estado: datos.domicilio_estado || ''
          });
          this.cargando.set(false);
        },
        error: (err) => {
          console.error('Error cargando datos:', err);
          this.error.set('No se pudieron cargar los datos del perfil');
          this.cargando.set(false);
        }
      });
  }

  // ==================== CARGAR ARCHIVOS PROTEGIDOS ====================
  private async cargarArchivos(datos: PerfilUsuario) {
    if (datos.foto_perfil) {
      const fotoUrl = await this.descargarArchivoProtegido(datos.foto_perfil);
      if (fotoUrl) {
        datos.foto_perfil = fotoUrl;
      }
    }
    
    if (datos.cv_archivo) {
      const cvUrl = await this.descargarArchivoProtegido(datos.cv_archivo);
      if (cvUrl) {
        datos.cv_archivo = cvUrl;
      }
    }
  }

  private async descargarArchivoProtegido(rutaArchivo: string): Promise<string | null> {
    try {
      const rutaNormalizada = this.normalizarRuta(rutaArchivo);
      
      const blob = await this.httpClient.get(rutaNormalizada, { 
        responseType: 'blob' 
      }).toPromise();
      
      if (!blob) return null;
      
      const objectUrl = URL.createObjectURL(blob);
      this.objectUrls.push(objectUrl);
      return objectUrl;
    } catch (err) {
      console.error('Error descargando archivo:', rutaArchivo, err);
      return null;
    }
  }

  private normalizarRuta(ruta: string): string {
    if (ruta.startsWith('http://') || ruta.startsWith('https://')) {
      return ruta;
    }
    
    if (ruta.startsWith('static/')) {
      const resto = ruta.replace('static/', '');
      const partes = resto.split('/');
      
      if (partes[0] === 'fotos') {
        return `${environment.apiBaseUrl}/archivos/fotos/${partes.slice(1).join('/')}`;
      } else if (partes[0] === 'cv') {
        return `${environment.apiBaseUrl}/archivos/cv/${partes.slice(1).join('/')}`;
      }
    }
    
    if (ruta.startsWith('/')) {
      return `${environment.apiBaseUrl}${ruta}`;
    }
    
    return `${environment.apiBaseUrl}/${ruta}`;
  }

  // ==================== TABS ====================
  cambiarTab(tab: 'datos' | 'documentos' | 'seguridad') {
    this.tabActiva.set(tab);
  }

  // ==================== EDITAR DATOS ====================
  habilitarEdicion() {
    this.editandoDatos.set(true);
  }

  cancelarEdicion() {
    this.editandoDatos.set(false);
    this.formDatos.reset();
    this.limpiarPrevisualizaciones();
    this.cargarDatos();
  }

  guardarDatos() {
    if (this.guardando()) return;
    
    if (!this.hayCambios()) {
      this.error.set('No hay cambios para guardar');
      return;
    }

    if (!confirm('¿Estás seguro de guardar los cambios en tu perfil?')) {
      return;
    }

    const formData = new FormData();
    
    // Campos de texto
    Object.keys(this.formDatos.value).forEach(key => {
      const valor = this.formDatos.value[key];
      if (valor !== null && valor !== '') {
        formData.append(key, valor);
      }
    });
    
    // Archivos
    if (this.fotoPreview()) {
      formData.append('foto_perfil', this.fotoPreview()!.file);
    }
    
    if (this.cvPreview()) {
      formData.append('cv_archivo', this.cvPreview()!.file);
    }
    
    if (this.documentosPreview().length > 0) {
      this.documentosPreview().forEach((doc, index) => {
        formData.append(`documentos_extra`, doc.file);
      });
    }
    
    this.guardando.set(true);
    this.error.set(null);
    
    this.httpClient.put<PerfilUsuario>(`${environment.apiBaseUrl}/perfil/me`, formData)
      .subscribe({
        next: (datos) => {
          this.successMsg.set('✓ Perfil actualizado correctamente');
          this.editandoDatos.set(false);
          this.limpiarPrevisualizaciones();
          this.formDatos.markAsPristine();
          this.guardando.set(false);
          
          setTimeout(() => {
            this.successMsg.set(null);
            this.cargarDatos();
          }, 2000);
        },
        error: (err) => {
          console.error('Error guardando datos:', err);
          this.error.set('Error al guardar los cambios. Intenta nuevamente.');
          this.guardando.set(false);
        }
      });
  }

  // ==================== MANEJO DE ARCHIVOS ====================
  onFotoSeleccionada(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files || !input.files[0]) return;

    const file = input.files[0];
    
    if (!file.type.startsWith('image/')) {
      this.error.set('Solo se permiten imágenes para la foto de perfil');
      return;
    }
    
    if (file.size > 5 * 1024 * 1024) {
      this.error.set('La imagen no debe superar 5MB');
      return;
    }

    // Mostrar modal de confirmación
    this.archivoEnConfirmacion.set({
      tipo: 'foto_perfil',
      nombre: file.name,
      file: file
    });
    this.mostrarModalConfirmacion.set(true);
  }

  onCvSeleccionado(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files || !input.files[0]) return;

    const file = input.files[0];
    
    if (file.type !== 'application/pdf') {
      this.error.set('El CV debe ser un archivo PDF');
      return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
      this.error.set('El CV no debe superar 10MB');
      return;
    }

    // Mostrar modal de confirmación
    this.archivoEnConfirmacion.set({
      tipo: 'cv_archivo',
      nombre: file.name,
      file: file
    });
    this.mostrarModalConfirmacion.set(true);
  }

  onDocumentosSeleccionados(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files || !input.files.length) return;

    // Procesar primer archivo seleccionado
    const file = input.files[0];
    const esPdf = file.type === 'application/pdf';
    const esImagen = file.type.startsWith('image/');
    
    if (!esPdf && !esImagen) {
      this.error.set('Solo se permiten archivos PDF o imágenes');
      return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
      this.error.set(`${file.name} supera el límite de 10MB`);
      return;
    }

    // Mostrar modal de confirmación
    this.archivoEnConfirmacion.set({
      tipo: 'documentos_extra',
      nombre: file.name,
      file: file
    });
    this.mostrarModalConfirmacion.set(true);
  }

  // ==================== MODAL CONFIRMACIÓN ====================
  cancelarConfirmacion() {
    this.mostrarModalConfirmacion.set(false);
    this.archivoEnConfirmacion.set(null);
  }

  confirmarSubida() {
    const archivo = this.archivoEnConfirmacion();
    if (!archivo) return;

    this.guardando.set(true);
    this.error.set(null);

    const formData = new FormData();
    formData.append(archivo.tipo, archivo.file);

    const endpoint = `${environment.apiBaseUrl}/perfil/me`;

    this.httpClient.put<PerfilUsuario>(endpoint, formData).subscribe({
      next: (datos) => {
        this.successMsg.set(`✓ ${archivo.nombre} subido correctamente`);
        this.guardando.set(false);
        this.mostrarModalConfirmacion.set(false);
        this.archivoEnConfirmacion.set(null);

        // Recargar datos después de 1.5 segundos
        setTimeout(() => {
          this.successMsg.set(null);
          this.cargarDatos();
        }, 1500);
      },
      error: (err) => {
        console.error('Error subiendo archivo:', err);
        this.error.set('Error al subir el archivo. Intenta nuevamente.');
        this.guardando.set(false);
      }
    });
  }

  eliminarFotoPreview() {
    const preview = this.fotoPreview();
    if (preview) {
      URL.revokeObjectURL(preview.preview);
      this.objectUrls = this.objectUrls.filter(url => url !== preview.preview);
    }
    this.fotoPreview.set(null);
  }

  eliminarCvPreview() {
    const preview = this.cvPreview();
    if (preview) {
      URL.revokeObjectURL(preview.preview);
      this.objectUrls = this.objectUrls.filter(url => url !== preview.preview);
    }
    this.cvPreview.set(null);
  }

  eliminarDocumentoPreview(index: number) {
    const docs = this.documentosPreview();
    const doc = docs[index];
    
    if (doc) {
      URL.revokeObjectURL(doc.preview);
      this.objectUrls = this.objectUrls.filter(url => url !== doc.preview);
    }
    
    docs.splice(index, 1);
    this.documentosPreview.set([...docs]);
  }

  private limpiarPrevisualizaciones() {
    this.eliminarFotoPreview();
    this.eliminarCvPreview();
    
    const docs = this.documentosPreview();
    docs.forEach(doc => {
      URL.revokeObjectURL(doc.preview);
    });
    
    this.documentosPreview.set([]);
  }

  private limpiarObjectUrls() {
    this.objectUrls.forEach(url => {
      URL.revokeObjectURL(url);
    });
    this.objectUrls = [];
  }

  // ==================== HELPERS ====================
  obtenerColorCompletitud(): string {
    const porcentaje = this.completitud();
    if (porcentaje < 50) return '#ef4444';
    if (porcentaje < 80) return '#f59e0b';
    return '#10b981';
  }

  formatearFecha(fecha: string | null | undefined): string {
    if (!fecha) return 'N/A';
    return new Date(fecha).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  getSafeUrl(url: string): SafeUrl {
    return this.sanitizer.bypassSecurityTrustUrl(url);
  }

  getNombreCompleto(): string {
    const datos = this.datosPersonales();
    if (!datos) return '';
    
    return `${datos.nombres} ${datos.apellido_paterno} ${datos.apellido_materno || ''}`.trim();
  }
}
