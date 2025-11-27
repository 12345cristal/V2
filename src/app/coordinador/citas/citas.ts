import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';

import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';

import { CitasService } from '../../service/citas.service';

import {
  CitaListado,
  CatalogosCitaResponse,
  EstadoCitaOpcion,
  EstadoCita,
  CrearCitaDto
} from '../interfaces/cita.interface';

@Component({
  selector: 'app-citas',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    MatIconModule
  ],
  templateUrl: './citas.html',
  styleUrls: ['./citas.scss']
})
export class CitasComponent implements OnInit {

  form!: FormGroup;

  citas: CitaListado[] = [];
  estadosCita: EstadoCitaOpcion[] = [];

  cargando = signal(false);
  cargandoCitas = signal(false);
  guardando = signal(false);

  mensajeExito = signal<string | null>(null);
  mensajeError = signal<string | null>(null);

  citaEnEdicion: CitaListado | null = null;

  // filtros
  filtroFecha: string | null = null;
  filtroEstado: EstadoCita | '' = '';
  filtroNino: string | null = null;

  // modal
  mostrarModal = signal(false);

  constructor(
    private fb: FormBuilder,
    private citasService: CitasService
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.cargarCatalogos();
  }

  // FORMULARIO NUEVO (sin terapias, sin ninoId)
  private initForm(): void {
    this.form = this.fb.group({
      nombreNino: ['', Validators.required],
      tutorNombre: ['', Validators.required],
      telefonoTutor1: ['', Validators.required],
      telefonoTutor2: [''],

      fecha: ['', Validators.required],
      horaInicio: ['', Validators.required],
      duracionMinutos: [50, [Validators.required, Validators.min(10)]],

      estadoId: [null, Validators.required],
      esReposicion: [false],
      citaOriginalId: [null],

      motivo: ['', [Validators.required, Validators.maxLength(255)]],
      diagnosticoPresuntivo: ['', Validators.maxLength(255)],
      observaciones: ['', Validators.maxLength(500)]
    });
  }

  // SOLO CARGA ESTADOS DE CITA
  private cargarCatalogos(): void {
    this.cargando.set(true);

    this.citasService.obtenerCatalogos().subscribe({
      next: (resp: CatalogosCitaResponse) => {
        this.estadosCita = resp.estadosCita;

        const estadoDefault = this.estadosCita.find(e => e.codigo === 'AGENDADA');
        if (estadoDefault) this.form.get('estadoId')?.setValue(estadoDefault.id);

        this.cargando.set(false);
        this.cargarCitas();
      },
      error: () => {
        this.mensajeError.set('Error al cargar catálogos.');
        this.cargando.set(false);
      }
    });
  }

  cargarCitas(): void {
    this.cargandoCitas.set(true);

    this.citasService.obtenerCitas(
      this.filtroFecha,
      this.filtroEstado || null,
      null
    ).subscribe({
      next: citas => {
        this.citas = citas;
        this.cargandoCitas.set(false);
      },
      error: () => {
        this.mensajeError.set('Error al cargar citas');
        this.cargandoCitas.set(false);
      }
    });
  }

  // ABRIR MODAL NUEVA CITA
  nuevaCita(): void {
    this.citaEnEdicion = null;

    this.form.reset({
      duracionMinutos: 50,
      esReposicion: false
    });

    const estadoDefault = this.estadosCita.find(e => e.codigo === 'AGENDADA');
    if (estadoDefault) {
      this.form.get('estadoId')?.setValue(estadoDefault.id);
    }

    this.mostrarModal.set(true);
  }

  cerrarModal(): void {
    this.mostrarModal.set(false);
  }

  // EDITAR (abre modal)
  editarCita(c: CitaListado): void {
    this.citaEnEdicion = c;

    const estado = this.estadosCita.find(e => e.codigo === c.estado);

    this.form.reset({
      nombreNino: c.nombreNino,
      tutorNombre: c.tutorNombre,
      telefonoTutor1: c.telefonoTutor1,
      telefonoTutor2: c.telefonoTutor2,

      fecha: c.fecha,
      horaInicio: c.horaInicio,
      duracionMinutos: this.calcularDuracion(c.horaInicio, c.horaFin),

      estadoId: estado?.id || null,
      esReposicion: c.esReposicion,

      motivo: c.motivo,
      diagnosticoPresuntivo: c.diagnosticoPresuntivo,
      observaciones: c.observaciones
    });

    this.mostrarModal.set(true);
  }

  calcularDuracion(hi: string, hf: string): number {
    if (!hi || !hf) return 50;

    const [h1, m1] = hi.split(':').map(Number);
    const [h2, m2] = hf.split(':').map(Number);

    return (h2 * 60 + m2) - (h1 * 60 + m1);
  }

  enviarFormulario(): void {
    this.mensajeExito.set(null);
    this.mensajeError.set(null);

    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const raw = this.form.getRawValue();

    const payload: CrearCitaDto = {
      nombreNino: raw.nombreNino,
      tutorNombre: raw.tutorNombre,
      telefonoTutor1: raw.telefonoTutor1,
      telefonoTutor2: raw.telefonoTutor2,

      fecha: raw.fecha,
      horaInicio: raw.horaInicio,
      duracionMinutos: raw.duracionMinutos,

      estadoId: raw.estadoId,
      esReposicion: raw.esReposicion,
      citaOriginalId: raw.citaOriginalId,

      motivo: raw.motivo,
      diagnosticoPresuntivo: raw.diagnosticoPresuntivo,
      observaciones: raw.observaciones
    };

    this.guardando.set(true);

    const peticion$ = this.citaEnEdicion
      ? this.citasService.actualizarCita(this.citaEnEdicion.id, { ...payload, id: this.citaEnEdicion.id })
      : this.citasService.crearCita(payload);

    peticion$.subscribe({
      next: () => {
        this.guardando.set(false);
        this.mensajeExito.set(
          this.citaEnEdicion ? 'Cita actualizada correctamente.' : 'Cita creada correctamente.'
        );
        this.cerrarModal();
        this.cargarCitas();
      },
      error: () => {
        this.guardando.set(false);
        this.mensajeError.set('Error al guardar cita');
      }
    });
  }

  aplicarFiltros(): void {
    this.cargarCitas();
  }

  limpiarFiltros(): void {
    this.filtroFecha = null;
    this.filtroEstado = '';
    this.filtroNino = null;
    this.cargarCitas();
  }

  cancelarCita(c: CitaListado): void {
    const motivo = prompt('Motivo de cancelación:');
    if (!motivo) return;

    this.citasService.cancelarCita(c.id, motivo).subscribe({
      next: () => {
        this.mensajeExito.set('Cita cancelada');
        this.cargarCitas();
      },
      error: () => {
        this.mensajeError.set('No se pudo cancelar la cita');
      }
    });
  }
}
