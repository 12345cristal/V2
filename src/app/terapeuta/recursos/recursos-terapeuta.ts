import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule
} from '@angular/forms';
import { RecursosTerapeutaService } from '../../service/recursos-terapeuta.service';

/* ===========================
   INTERFACES LOCALES
=========================== */
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

  /* ===========================
     STATE
  =========================== */
  recursos = signal<Recurso[]>([]);
  hijos = signal<Hijo[]>([]);

  cargando = signal(false);
  cargandoHijos = signal(false);
  subiendoArchivo = signal(false);
  error = signal<string | null>(null);

  mostrarFormulario = signal(false);
  modoEdicion = signal(false);
  recursoEditando = signal<number | null>(null);

  archivoSeleccionado = signal<File | null>(null);
  previsualizacionArchivo = signal<string | null>(null);

  /* ===========================
     FORM
  =========================== */
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

  /* ===========================
     COMPUTED
  =========================== */
  recursosTotal = computed(() => this.recursos().length);
  recursosRecientes = computed(() => this.recursos().slice(0, 5));

  recursosPorCategoria = computed(() => {
    const map = new Map<string, number>();
    this.recursos().forEach(r => {
      map.set(r.categoria_recurso, (map.get(r.categoria_recurso) || 0) + 1);
    });
    return map;
  });

  constructor(
    private fb: FormBuilder,
    private recursosService: RecursosTerapeutaService
  ) {
    this.formulario = this.fb.group({
      titulo: ['', [Validators.required, Validators.maxLength(255)]],
      descripcion: ['', Validators.required],
      tipo_recurso: ['PDF', Validators.required],
      categoria_recurso: ['', Validators.required],
      nivel_recurso: ['', Validators.required],
      objetivo_terapeutico: ['', Validators.required],
      hijo_id: ['', Validators.required],
      url: ['']
    });

    /* Validación dinámica de URL */
    this.formulario.get('tipo_recurso')?.valueChanges.subscribe((tipo) => {
      const url = this.formulario.get('url');
      if (tipo === 'VIDEO' || tipo === 'ENLACE') {
        url?.setValidators([
          Validators.required,
          Validators.pattern(/^https?:\/\/.+/)
        ]);
      } else {
        url?.clearValidators();
      }
      url?.updateValueAndValidity();
    });
  }

  /* ===========================
     INIT
  =========================== */
  ngOnInit(): void {
    this.cargarRecursos();
    this.cargarHijos();
  }

  /* ===========================
     DATA
  =========================== */
  cargarRecursos(): void {
    this.cargando.set(true);
    this.error.set(null);

    this.recursosService.obtenerMisRecursos().subscribe({
      next: (data) => {
        this.recursos.set(data);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('Error al cargar recursos');
        this.cargando.set(false);
      }
    });
  }

  cargarHijos(): void {
    this.cargandoHijos.set(true);

    this.recursosService.obtenerHijosPacientes().subscribe({
      next: (data) => {
        this.hijos.set(data);
        this.cargandoHijos.set(false);
      },
      error: () => {
        this.cargandoHijos.set(false);
      }
    });
  }

  /* ===========================
     FORM ACTIONS
  =========================== */
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
    const archivo = input.files?.[0];
    if (!archivo) return;

    if (
      this.formulario.value.tipo_recurso === 'PDF' &&
      archivo.type !== 'application/pdf'
    ) {
      this.error.set('Solo se permiten archivos PDF');
      return;
    }

    this.archivoSeleccionado.set(archivo);

    if (archivo.type === 'application/pdf') {
      const reader = new FileReader();
      reader.onload = () =>
        this.previsualizacionArchivo.set(reader.result as string);
      reader.readAsDataURL(archivo);
    }
  }

  guardarRecurso(): void {
    if (this.formulario.invalid) {
      this.formulario.markAllAsTouched();
      return;
    }

    const tipo = this.formulario.value.tipo_recurso;

    if (tipo === 'PDF' && !this.archivoSeleccionado()) {
      this.error.set('Debes subir un archivo PDF');
      return;
    }

    if ((tipo === 'VIDEO' || tipo === 'ENLACE') && !this.formulario.value.url) {
      this.error.set('Debes proporcionar una URL válida');
      return;
    }

    this.subiendoArchivo.set(true);
    this.error.set(null);
const formData = new FormData();

Object.entries(this.formulario.value).forEach(([key, value]) => {
  if (value !== null && value !== undefined && value !== '') {
    formData.append(key, String(value));
  }
});

if (this.archivoSeleccionado()) {
  formData.append('archivo', this.archivoSeleccionado()!);
}


    if (this.archivoSeleccionado()) {
      formData.append('archivo', this.archivoSeleccionado()!);
    }

    this.recursosService.crearRecurso(formData).subscribe({
      next: () => {
        this.subiendoArchivo.set(false);
        this.cerrarFormulario();
        this.cargarRecursos();
      },
      error: () => {
        this.subiendoArchivo.set(false);
        this.error.set('Error al guardar el recurso');
      }
    });
  }

  eliminarRecurso(id: number): void {
    if (!confirm('¿Eliminar este recurso?')) return;

    this.recursosService.eliminarRecurso(id).subscribe({
      next: () => {
        this.recursos.update(list => list.filter(r => r.id !== id));
      },
      error: () => {
        this.error.set('Error al eliminar el recurso');
      }
    });
  }

  /* ===========================
     ACTIONS
  =========================== */
  verRecurso(r: Recurso): void {
    if (r.tipo_recurso === 'PDF' && r.archivo) {
      window.open(r.archivo, '_blank');
    } else if (r.url) {
      window.open(r.url, '_blank');
    }
  }

  descargarRecurso(r: Recurso): void {
    this.recursosService.descargarRecurso(r.archivo);
  }

  /* ===========================
     HELPERS
  =========================== */
  getIconoTipo(tipo: string): string {
    return { PDF: '📄', VIDEO: '🎥', ENLACE: '🔗' }[tipo] ?? '📋';
  }

  getColorCategoria(cat: string): string {
    return {
      Comunicación: 'azul',
      Social: 'verde',
      Conducta: 'naranja',
      Sensorial: 'morado',
      Cognitivo: 'rosa',
      Autonomía: 'cyan',
      Académico: 'amarillo'
    }[cat] ?? 'gris';
  }

  campoInvalido(campo: string): boolean {
    const c = this.formulario.get(campo);
    return !!(c && c.invalid && c.touched);
  }

  getMensajeError(campo: string): string {
    const c = this.formulario.get(campo);
    if (c?.hasError('required')) return 'Campo obligatorio';
    if (c?.hasError('pattern')) return 'URL inválida';
    if (c?.hasError('maxlength')) return 'Máx. 255 caracteres';
    return '';
  }
}
