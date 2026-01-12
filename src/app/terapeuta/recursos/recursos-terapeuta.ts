import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule
} from '@angular/forms';
import { RecursosTerapeutaService } from '../../service/recursos-terapeuta.service';

interface Recurso {
  id: number;
  titulo: string;
  descripcion: string;
  tipo_recurso: 'PDF' | 'VIDEO' | 'ENLACE';
  categoria_recurso: string;
  nivel_recurso: string;
  url: string;
  archivo: string | null;
  objetivo_terapeutico: string;
  fecha_creacion: string;
  asignaciones: number;
}

interface Hijo {
  id: number;
  nombre: string;
  apellido: string;
  edad: number;
  padre_nombre: string;
  padre_id: number;
}

@Component({
  selector: 'app-recursos-terapeuta',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './recursos-terapeuta.html',
  styleUrls: ['./recursos-terapeuta.scss']
})
export class RecursosTerapeutaComponent implements OnInit {
  recursos = signal<Recurso[]>([]);
  hijos = signal<Hijo[]>([]);
  cargando = signal<boolean>(false);
  cargandoHijos = signal<boolean>(false);
  error = signal<string | null>(null);

  mostrarFormulario = signal<boolean>(false);
  modoEdicion = signal<boolean>(false);
  recursoEditando = signal<number | null>(null);

  archivoSeleccionado = signal<File | null>(null);
  previsualizacionArchivo = signal<string | null>(null);
  subiendoArchivo = signal<boolean>(false);

  formulario: FormGroup;

  categorias = [
    'Comunicación',
    'Social',
    'Conducta',
    'Sensorial',
    'Cognitivo',
    'Autonomía',
    'Académico'
  ];

  niveles = ['Básico', 'Intermedio', 'Avanzado'];

  recursosTotal = computed(() => this.recursos().length);

  recursosRecientes = computed(() => this.recursos().slice(0, 5));

  recursosPorCategoria = computed(() => {
    const categorias = new Map<string, number>();
    this.recursos().forEach((r) => {
      const categoria = r.categoria_recurso;
      categorias.set(categoria, (categorias.get(categoria) || 0) + 1);
    });
    return categorias;
  });

  constructor(
    private fb: FormBuilder,
    private recursosService: RecursosTerapeutaService
  ) {
    this.formulario = this.fb.group({
      titulo: ['', [Validators.required, Validators.maxLength(255)]],
      descripcion: ['', [Validators.required]],
      tipo_recurso: ['PDF', [Validators.required]],
      categoria_recurso: ['', [Validators.required]],
      nivel_recurso: ['', [Validators.required]],
      objetivo_terapeutico: ['', [Validators.required]],
      hijo_id: ['', [Validators.required]],
      url: ['']
    });

    // Validación dinámica de URL según tipo
    this.formulario.get('tipo_recurso')?.valueChanges.subscribe((tipo: string) => {
      const urlControl = this.formulario.get('url');
      if (tipo === 'VIDEO' || tipo === 'ENLACE') {
        urlControl?.setValidators([
          Validators.required,
          Validators.pattern(/^https?:\/\/.+/)
        ]);
      } else {
        urlControl?.clearValidators();
      }
      urlControl?.updateValueAndValidity();
    });
  }

  ngOnInit(): void {
    this.cargarRecursos();
    this.cargarHijos();
  }

  cargarRecursos(): void {
    this.cargando.set(true);
    this.error.set(null);

    this.recursosService.obtenerMisRecursos().subscribe({
      next: (datos: Recurso[]) => {
        this.recursos.set(datos);
        this.cargando.set(false);
      },
      error: (err: Error) => {
        this.error.set('Error al cargar recursos');
        this.cargando.set(false);
        console.error('Error:', err);
      }
    });
  }

  cargarHijos(): void {
    this.cargandoHijos.set(true);

    this.recursosService.obtenerHijosPacientes().subscribe({
      next: (datos: Hijo[]) => {
        this.hijos.set(datos);
        this.cargandoHijos.set(false);
      },
      error: (err: Error) => {
        console.error('Error al cargar hijos:', err);
        this.cargandoHijos.set(false);
      }
    });
  }

  abrirFormulario(): void {
    this.mostrarFormulario.set(true);
    this.modoEdicion.set(false);
    this.formulario.reset({ tipo_recurso: 'PDF' });
    this.archivoSeleccionado.set(null);
    this.previsualizacionArchivo.set(null);
  }

  cerrarFormulario(): void {
    this.mostrarFormulario.set(false);
    this.modoEdicion.set(false);
    this.recursoEditando.set(null);
    this.formulario.reset();
    this.archivoSeleccionado.set(null);
    this.previsualizacionArchivo.set(null);
  }

  seleccionarArchivo(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const archivo = input.files[0];

      // Validar tipo de archivo
      if (
        this.formulario.value.tipo_recurso === 'PDF' &&
        archivo.type !== 'application/pdf'
      ) {
        this.error.set('Por favor selecciona un archivo PDF válido');
        return;
      }

      this.archivoSeleccionado.set(archivo);

      // Previsualización para PDFs
      if (archivo.type === 'application/pdf') {
        const reader = new FileReader();
        reader.onload = (e: ProgressEvent<FileReader>) => {
          this.previsualizacionArchivo.set(
            e.target?.result as string
          );
        };
        reader.readAsDataURL(archivo);
      }
    }
  }

  guardarRecurso(): void {
    if (this.formulario.invalid) {
      Object.keys(this.formulario.controls).forEach((key) => {
        this.formulario.get(key)?.markAsTouched();
      });
      return;
    }

    const tipoRecurso = this.formulario.value.tipo_recurso;

    // Validar archivo para PDF
    if (
      tipoRecurso === 'PDF' &&
      !this.archivoSeleccionado() &&
      !this.modoEdicion()
    ) {
      this.error.set('Debes seleccionar un archivo PDF');
      return;
    }

    // Validar URL para VIDEO y ENLACE
    if (
      (tipoRecurso === 'VIDEO' || tipoRecurso === 'ENLACE') &&
      !this.formulario.value.url
    ) {
      this.error.set('Debes proporcionar una URL válida');
      return;
    }

    this.subiendoArchivo.set(true);
    this.error.set(null);

    const formData = new FormData();
    Object.keys(this.formulario.value).forEach((key) => {
      if (this.formulario.value[key]) {
        formData.append(key, this.formulario.value[key]);
      }
    });

    if (this.archivoSeleccionado()) {
      formData.append('archivo', this.archivoSeleccionado()!);
    }

    this.recursosService.crearRecurso(formData).subscribe({
      next: (response: any) => {
        this.subiendoArchivo.set(false);
        this.cerrarFormulario();
        this.cargarRecursos();
        this.mostrarMensajeExito('Recurso creado exitosamente');
      },
      error: (err: Error) => {
        this.subiendoArchivo.set(false);
        this.error.set(
          'Error al guardar el recurso. Intenta nuevamente.'
        );
        console.error('Error:', err);
      }
    });
  }

  eliminarRecurso(id: number): void {
    if (
      !confirm(
        '¿Estás seguro de eliminar este recurso? Esta acción no se puede deshacer.'
      )
    ) {
      return;
    }

    this.recursosService.eliminarRecurso(id).subscribe({
      next: () => {
        this.recursos.update((recursos) =>
          recursos.filter((r) => r.id !== id)
        );
        this.mostrarMensajeExito('Recurso eliminado correctamente');
      },
      error: (err: Error) => {
        this.error.set('Error al eliminar el recurso');
        console.error('Error:', err);
      }
    });
  }

  verRecurso(recurso: Recurso): void {
    if (recurso.tipo_recurso === 'PDF' && recurso.archivo) {
      window.open(recurso.archivo, '_blank');
    } else if (recurso.url) {
      window.open(recurso.url, '_blank');
    }
  }

  descargarRecurso(recurso: Recurso): void {
    if (recurso.archivo) {
      this.recursosService.descargarRecurso(recurso.archivo);
    }
  }

  getIconoTipo(tipo: string): string {
    const iconos: { [key: string]: string } = {
      'PDF': '📄',
      'VIDEO': '🎥',
      'ENLACE': '🔗'
    };
    return iconos[tipo] || '📋';
  }

  getColorCategoria(categoria: string): string {
    const colores: { [key: string]: string } = {
      'Comunicación': 'azul',
      'Social': 'verde',
      'Conducta': 'naranja',
      'Sensorial': 'morado',
      'Cognitivo': 'rosa',
      'Autonomía': 'cyan',
      'Académico': 'amarillo'
    };
    return colores[categoria] || 'gris';
  }

  private mostrarMensajeExito(mensaje: string): void {
    console.log(mensaje);
  }

  campoInvalido(campo: string): boolean {
    const control = this.formulario.get(campo);
    return !!(control && control.invalid && control.touched);
  }

  getMensajeError(campo: string): string {
    const control = this.formulario.get(campo);
    if (control?.hasError('required')) {
      return 'Este campo es obligatorio';
    }
    if (control?.hasError('pattern')) {
      return 'URL inválida';
    }
    if (control?.hasError('maxlength')) {
      return 'Máximo 255 caracteres';
    }
    return '';
  }
}
