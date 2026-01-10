import { Component, OnInit, computed, signal, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { HttpClient } from '@angular/common/http';

interface DatosPersonales {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  telefono?: string;
  direccion?: string;
  ciudad?: string;
  fecha_ingreso?: string;
}

interface Documento {
  id: number;
  tipo: 'CV' | 'CERTIFICADO' | 'OTRO';
  nombre: string;
  url: string;
  fecha_carga: string;
}

interface DatosCompletos extends DatosPersonales {
  documentos: Documento[];
  foto_perfil?: string;
  roles: string[];
  estado: 'ACTIVO' | 'INACTIVO';
}

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatIconModule],
  templateUrl: './perfil.html',
  styleUrl: './perfil.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PerfilComponent implements OnInit {
  private httpClient = inject(HttpClient);
  private fb = inject(FormBuilder);

  // ==================== SIGNALS ====================
  datosPersonales = signal<DatosCompletos | null>(null);
  cargando = signal(false);
  error = signal<string | null>(null);
  
  tabActiva = signal<'datos' | 'documentos' | 'seguridad'>('datos');
  editandoDatos = signal(false);
  mostrarModalPassword = signal(false);
  
  formDatos: FormGroup;
  formPassword: FormGroup;

  // ==================== COMPUTED ====================
  documentosFaltantes = computed(() => {
    const datos = this.datosPersonales();
    if (!datos) return [];
    
    const faltantes: string[] = [];
    
    // Verificar CV
    if (!datos.documentos.find(d => d.tipo === 'CV')) {
      faltantes.push('Falta CV');
    }
    
    // Verificar foto
    if (!datos.foto_perfil) {
      faltantes.push('Falta foto de perfil');
    }
    
    // Verificar certificados
    if (datos.documentos.filter(d => d.tipo === 'CERTIFICADO').length === 0) {
      faltantes.push('Falta al menos un certificado');
    }
    
    return faltantes;
  });

  completitud = computed(() => {
    const datos = this.datosPersonales();
    if (!datos) return 0;
    
    let items = 0;
    let completados = 0;
    
    // Verificar datos básicos
    items += 4;
    if (datos.nombre) completados++;
    if (datos.apellido) completados++;
    if (datos.email) completados++;
    if (datos.telefono) completados++;
    
    // Verificar contacto
    items += 2;
    if (datos.ciudad) completados++;
    if (datos.direccion) completados++;
    
    // Verificar documentos
    items += 3;
    if (datos.documentos.find(d => d.tipo === 'CV')) completados++;
    if (datos.foto_perfil) completados++;
    if (datos.documentos.find(d => d.tipo === 'CERTIFICADO')) completados++;
    
    return Math.round((completados / items) * 100);
  });

  constructor() {
    this.formDatos = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(2)]],
      apellido: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      telefono: [''],
      ciudad: [''],
      direccion: ['']
    });

    this.formPassword = this.fb.group({
      passwordActual: ['', [Validators.required, Validators.minLength(6)]],
      passwordNueva: ['', [Validators.required, Validators.minLength(6)]],
      confirmarPassword: ['', Validators.required]
    }, { validators: this.passwordsIgualesValidator() });
  }

  ngOnInit() {
    this.cargarDatos();
  }

  // ==================== MÉTODOS ====================
  cargarDatos() {
    this.cargando.set(true);
    this.error.set(null);
    
    this.httpClient.get<DatosCompletos>('/api/perfil/datos')
      .subscribe({
        next: (datos) => {
          this.datosPersonales.set(datos);
          this.formDatos.patchValue({
            nombre: datos.nombre,
            apellido: datos.apellido,
            email: datos.email,
            telefono: datos.telefono || '',
            ciudad: datos.ciudad || '',
            direccion: datos.direccion || ''
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

  cambiarTab(tab: 'datos' | 'documentos' | 'seguridad') {
    this.tabActiva.set(tab);
  }

  // ==================== EDITAR DATOS ====================
  habilitarEdicion() {
    this.editandoDatos.set(true);
  }

  cancelarEdicion() {
    this.editandoDatos.set(false);
    this.cargarDatos();
  }

  guardarDatos() {
    if (!this.formDatos.valid) return;

    const datos = this.formDatos.value;
    
    this.httpClient.put('/api/perfil/datos', datos)
      .subscribe({
        next: () => {
          this.editandoDatos.set(false);
          this.cargarDatos();
        },
        error: (err) => {
          console.error('Error guardando datos:', err);
          this.error.set('No se pudieron guardar los cambios');
        }
      });
  }

  // ==================== CAMBIAR CONTRASEÑA ====================
  abrirModalPassword() {
    this.formPassword.reset();
    this.mostrarModalPassword.set(true);
  }

  cerrarModalPassword() {
    this.mostrarModalPassword.set(false);
    this.formPassword.reset();
  }

  cambiarPassword() {
    if (!this.formPassword.valid) return;

    const datos = this.formPassword.value;
    
    this.httpClient.post('/api/perfil/cambiar-password', {
      password_actual: datos.passwordActual,
      password_nueva: datos.passwordNueva
    }).subscribe({
      next: () => {
        this.cerrarModalPassword();
        // Mostrar mensaje de éxito
      },
      error: (err) => {
        console.error('Error cambiando contraseña:', err);
        this.error.set('Error al cambiar la contraseña');
      }
    });
  }

  // ==================== DOCUMENTOS ====================
  subirDocumento(tipo: 'CV' | 'CERTIFICADO', event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files || !input.files[0]) return;

    const formData = new FormData();
    formData.append('archivo', input.files[0]);
    formData.append('tipo', tipo);

    this.httpClient.post<Documento>('/api/perfil/documentos', formData)
      .subscribe({
        next: () => {
          this.cargarDatos();
        },
        error: (err) => {
          console.error('Error subiendo documento:', err);
          this.error.set('Error al subir el documento');
        }
      });
  }

  subirFoto(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files || !input.files[0]) return;

    const formData = new FormData();
    formData.append('archivo', input.files[0]);

    this.httpClient.post('/api/perfil/foto', formData)
      .subscribe({
        next: () => {
          this.cargarDatos();
        },
        error: (err) => {
          console.error('Error subiendo foto:', err);
          this.error.set('Error al subir la foto');
        }
      });
  }

  eliminarDocumento(docId: number) {
    this.httpClient.delete(`/api/perfil/documentos/${docId}`)
      .subscribe({
        next: () => {
          this.cargarDatos();
        },
        error: (err) => {
          console.error('Error eliminando documento:', err);
        }
      });
  }

  descargarDocumento(doc: Documento) {
    window.open(doc.url, '_blank');
  }

  // ==================== HELPERS ====================
  passwordsIgualesValidator() {
    return (group: FormGroup) => {
      const password = group.get('passwordNueva')?.value;
      const confirmar = group.get('confirmarPassword')?.value;

      if (password !== confirmar) {
        group.get('confirmarPassword')?.setErrors({ 'mismatch': true });
      }
      return null;
    };
  }

  obtenerIconoDocumento(tipo: string): string {
    const iconos: { [key: string]: string } = {
      'CV': 'description',
      'CERTIFICADO': 'verified',
      'OTRO': 'file_present'
    };
    return iconos[tipo] || 'file_present';
  }

  obtenerColorCompletitud(): string {
    const porcentaje = this.completitud();
    if (porcentaje < 50) return '#ef4444';
    if (porcentaje < 80) return '#f59e0b';
    return '#10b981';
  }

  formatearFecha(fecha: string | undefined): string {
    if (!fecha) return 'N/A';
    return new Date(fecha).toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
}
