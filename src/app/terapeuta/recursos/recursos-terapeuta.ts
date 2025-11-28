import {
  Component,
  OnInit,
  signal,
  computed
} from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';

import {
  RecursoTerapeuta,
  NinoResumen,
  TareaAsignada,
  OpcionFiltro,
  CrearRecursoDto,
  ActualizarRecursoDto,
  CrearTareaDto
} from '../../interfaces/recurso-terapeuta.interface';

import { RecursosTerapeutaService } from '../../service/recursos-terapeuta.service';

@Component({
  selector: 'app-recursos-terapeuta',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatIconModule],
  templateUrl: './recursos-terapeuta.html',
  styleUrls: ['./recursos-terapeuta.scss']
})
export class RecursosTerapeutaComponent implements OnInit {

  // ======= Signals de estado =======
  cargando = signal(false);
  cargandoDestacados = signal(false);
  cargandoFiltros = signal(false);
  cargandoTareas = signal(false);

  recursos = signal<RecursoTerapeuta[]>([]);
  recursosDestacados = signal<RecursoTerapeuta[]>([]);
  tareasRecurso = signal<TareaAsignada[]>([]);
  ninosAsignables = signal<NinoResumen[]>([]);

  tipos = signal<OpcionFiltro[]>([]);
  categorias = signal<OpcionFiltro[]>([]);
  niveles = signal<OpcionFiltro[]>([]);
  estados = signal<OpcionFiltro[]>([]);

  recursoSeleccionado = signal<RecursoTerapeuta | null>(null);

  mostrarModalRecurso = signal(false);
  mostrarModalTareas = signal(false);
  modoEdicion = signal(false);

  mensajeExito = signal<string | null>(null);
  mensajeError = signal<string | null>(null);

  // ======= Formularios =======
  filtrosForm: FormGroup;
  recursoForm: FormGroup;
  tareaForm: FormGroup;

  tituloModalRecurso = computed(() =>
    this.modoEdicion() ? 'Editar recurso' : 'Nuevo recurso'
  );

  constructor(
    private fb: FormBuilder,
    private recursosService: RecursosTerapeutaService
  ) {
    this.filtrosForm = this.fb.group({
      texto: [''],
      categoriaId: ['todos'],
      estadoId: ['todos']
    });

    this.recursoForm = this.fb.group({
      titulo: ['', [Validators.required, Validators.maxLength(120)]],
      descripcion: ['', [Validators.required, Validators.maxLength(500)]],
      tipoId: ['', Validators.required],
      categoriaId: ['', Validators.required],
      nivelId: ['', Validators.required],
      etiquetas: [''],
      esDestacado: [false],
      esNuevo: [true]
    });

    this.tareaForm = this.fb.group({
      ninosIds: [[], Validators.required],
      fechaLimite: [''],
      notasTerapeuta: ['']
    });
  }

  ngOnInit(): void {
    this.cargarFiltros();
    this.cargarRecursos();
    this.cargarDestacados();
    this.cargarNinos();

    this.filtrosForm.valueChanges.subscribe(() => {
      this.cargarRecursos();
    });
  }

  // ================== CARGA DE DATOS ==================

  cargarFiltros(): void {
    this.cargandoFiltros.set(true);
    this.recursosService.getFiltros().subscribe({
      next: (res) => {
        this.tipos.set(res.tipos ?? []);
        this.categorias.set(res.categorias ?? []);
        this.niveles.set(res.niveles ?? []);
        this.estados.set(res.estados ?? []);
        this.cargandoFiltros.set(false);
      },
      error: () => {
        this.cargandoFiltros.set(false);
        this.mostrarError('No se pudieron cargar los filtros.');
      }
    });
  }

  cargarRecursos(): void {
    this.cargando.set(true);
    const { texto, categoriaId, estadoId } = this.filtrosForm.value;

    this.recursosService.getRecursos({
      texto: texto || undefined,
      categoriaId: categoriaId || undefined,
      estadoId: estadoId || undefined
    }).subscribe({
      next: (res) => {
        this.recursos.set(res);
        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
        this.mostrarError('No se pudieron cargar los recursos.');
      }
    });
  }

  cargarDestacados(): void {
    this.cargandoDestacados.set(true);
    this.recursosService.getRecursosDestacados().subscribe({
      next: (res) => {
        this.recursosDestacados.set(res);
        this.cargandoDestacados.set(false);
      },
      error: () => {
        this.cargandoDestacados.set(false);
      }
    });
  }

  cargarNinos(): void {
    this.recursosService.getNinosAsignables().subscribe({
      next: (res) => this.ninosAsignables.set(res),
      error: () => {}
    });
  }

  cargarTareas(recurso: RecursoTerapeuta): void {
    this.cargandoTareas.set(true);
    this.recursosService.getTareasPorRecurso(recurso.id).subscribe({
      next: (res) => {
        this.tareasRecurso.set(res);
        this.cargandoTareas.set(false);
      },
      error: () => {
        this.cargandoTareas.set(false);
        this.mostrarError('No se pudieron cargar las tareas asignadas.');
      }
    });
  }

  // ================== UI / ACCIONES ==================

  refrescar(): void {
    this.cargarRecursos();
    this.cargarDestacados();
  }

  nuevoRecurso(): void {
    this.modoEdicion.set(false);
    this.recursoSeleccionado.set(null);
    this.recursoForm.reset({
      esDestacado: false,
      esNuevo: true
    });
    this.mostrarModalRecurso.set(true);
  }

  editarRecurso(recurso: RecursoTerapeuta): void {
    this.modoEdicion.set(true);
    this.recursoSeleccionado.set(recurso);

    this.recursoForm.patchValue({
      titulo: recurso.titulo,
      descripcion: recurso.descripcion,
      tipoId: recurso.tipoId,
      categoriaId: recurso.categoriaId,
      nivelId: recurso.nivelId,
      etiquetas: recurso.etiquetas?.join(', '),
      esDestacado: recurso.esDestacado,
      esNuevo: recurso.esNuevo
    });

    this.mostrarModalRecurso.set(true);
  }

  cerrarModalRecurso(): void {
    this.mostrarModalRecurso.set(false);
  }

  abrirModalTareas(recurso: RecursoTerapeuta): void {
    this.recursoSeleccionado.set(recurso);
    this.tareaForm.reset({
      ninosIds: [],
      fechaLimite: '',
      notasTerapeuta: ''
    });
    this.cargarTareas(recurso);
    this.mostrarModalTareas.set(true);
  }

  cerrarModalTareas(): void {
    this.mostrarModalTareas.set(false);
  }

  // ================== GUARDAR / ELIMINAR ==================

  guardarRecurso(): void {
    if (this.recursoForm.invalid) {
      this.recursoForm.markAllAsTouched();
      return;
    }

    const formValue = this.recursoForm.value;

    const etiquetas = (formValue.etiquetas || '')
      .split(',')
      .map((e: string) => e.trim())
      .filter((e: string) => !!e);

    const payload: CrearRecursoDto = {
      titulo: formValue.titulo,
      descripcion: formValue.descripcion,
      tipoId: formValue.tipoId,
      categoriaId: formValue.categoriaId,
      nivelId: formValue.nivelId,
      etiquetas,
      esDestacado: !!formValue.esDestacado,
      esNuevo: !!formValue.esNuevo
    };

    if (this.modoEdicion() && this.recursoSeleccionado()) {
      const updatePayload: ActualizarRecursoDto = {
        ...payload,
        id: this.recursoSeleccionado()!.id
      };

      this.recursosService.actualizarRecurso(updatePayload.id, updatePayload).subscribe({
        next: () => {
          this.mostrarExito('Recurso actualizado correctamente.');
          this.cerrarModalRecurso();
          this.cargarRecursos();
          this.cargarDestacados();
        },
        error: () => this.mostrarError('No se pudo actualizar el recurso.')
      });
    } else {
      this.recursosService.crearRecurso(payload).subscribe({
        next: () => {
          this.mostrarExito('Recurso creado correctamente.');
          this.cerrarModalRecurso();
          this.cargarRecursos();
          this.cargarDestacados();
        },
        error: () => this.mostrarError('No se pudo crear el recurso.')
      });
    }
  }

  eliminarRecurso(recurso: RecursoTerapeuta): void {
    const confirmar = window.confirm(
      `¿Eliminar el recurso "${recurso.titulo}"? Esta acción no se puede deshacer.`
    );
    if (!confirmar) return;

    this.recursosService.eliminarRecurso(recurso.id).subscribe({
      next: () => {
        this.mostrarExito('Recurso eliminado.');
        this.cargarRecursos();
        this.cargarDestacados();
      },
      error: () => this.mostrarError('No se pudo eliminar el recurso.')
    });
  }

  asignarTarea(): void {
    if (!this.recursoSeleccionado()) return;
    if (this.tareaForm.invalid) {
      this.tareaForm.markAllAsTouched();
      return;
    }

    const { ninosIds, fechaLimite, notasTerapeuta } = this.tareaForm.value;

    const dto: CrearTareaDto = {
      recursoId: this.recursoSeleccionado()!.id,
      ninosIds: (ninosIds || []).map((id: string | number) => Number(id)),
      fechaLimite: fechaLimite || null,
      notasTerapeuta: notasTerapeuta || null
    };

    this.recursosService.crearTareas(dto).subscribe({
      next: () => {
        this.mostrarExito('Tarea asignada correctamente.');
        this.cargarTareas(this.recursoSeleccionado()!);
        this.tareaForm.reset({
          ninosIds: [],
          fechaLimite: '',
          notasTerapeuta: ''
        });
      },
      error: () => this.mostrarError('No se pudo asignar la tarea.')
    });
  }

  toggleCompleto(tarea: TareaAsignada): void {
    this.recursosService.actualizarTarea(tarea.id, {
      completado: !tarea.completado
    }).subscribe({
      next: (resp) => {
        // actualiza en memoria
        const lista = this.tareasRecurso().map(t =>
          t.id === resp.id ? resp : t
        );
        this.tareasRecurso.set(lista);
      },
      error: () => this.mostrarError('No se pudo actualizar el estado de la tarea.')
    });
  }

  // ================== HELPERS ==================

  progreso(recurso: RecursoTerapeuta): number {
    if (!recurso.totalAsignaciones) return 0;
    return Math.round((recurso.totalCompletadas / recurso.totalAsignaciones) * 100);
  }

  mostrarExito(msg: string): void {
    this.mensajeExito.set(msg);
    this.mensajeError.set(null);
    setTimeout(() => this.mensajeExito.set(null), 4000);
  }

  mostrarError(msg: string): void {
    this.mensajeError.set(msg);
    this.mensajeExito.set(null);
    setTimeout(() => this.mensajeError.set(null), 5000);
  }
}
