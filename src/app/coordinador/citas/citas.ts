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
import { NotificationService } from '../../shared/notification.service';

import {
  Cita,
  CitaCreate,
  CitaUpdate,
  EstadoCitaCatalogo,
  CitaFiltros
} from '../../interfaces/cita.interface';

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

  citas: Cita[] = [];
  estadosCita: EstadoCitaCatalogo[] = [];

  cargando = signal(false);
  cargandoCitas = signal(false);
  guardando = signal(false);

  citaEnEdicion: Cita | null = null;

  // Paginación
  totalCitas = 0;
  paginaActual = 1;
  tamanioPagina = 20;
  totalPaginas = 0;

  // Filtros
  filtros: CitaFiltros = {
    page: 1,
    page_size: 20
  };

  filtroFecha: string = '';
  filtroEstado: number | '' = '';
  filtroBuscar: string = '';

  // Modal
  mostrarModal = signal(false);

  constructor(
    private fb: FormBuilder,
    private citasService: CitasService,
    private notificationService: NotificationService
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.cargarEstadosCita();
    this.cargarCitas();
  }

  private initForm(): void {
    this.form = this.fb.group({
      nino_id: [null, Validators.required],
      terapeuta_id: [null, Validators.required],
      terapia_id: [null, Validators.required],
      fecha: ['', Validators.required],
      hora_inicio: ['', Validators.required],
      hora_fin: ['', Validators.required],
      estado_id: [1],  // PROGRAMADA por defecto
      motivo: [''],
      observaciones: [''],
      es_reposicion: [0]
    });
  }

  private cargarEstadosCita(): void {
    this.citasService.getEstadosCita().subscribe({
      next: (estados) => {
        this.estadosCita = estados;
        console.log('Estados de cita cargados:', estados);
      },
      error: (err) => {
        console.error('Error al cargar estados de cita:', err);
        this.notificationService.error('Error al cargar estados de cita');
      }
    });
  }

  cargarCitas(): void {
    this.cargandoCitas.set(true);

    // Construir filtros
    const filtros: CitaFiltros = {
      page: this.paginaActual,
      page_size: this.tamanioPagina
    };

    if (this.filtroFecha) {
      filtros.fecha = this.filtroFecha;
    }

    if (this.filtroEstado !== '') {
      filtros.estado_id = Number(this.filtroEstado);
    }

    if (this.filtroBuscar) {
      filtros.buscar = this.filtroBuscar;
    }

    console.log('Cargando citas con filtros:', filtros);

    this.citasService.getCitas(filtros).subscribe({
      next: (response) => {
        this.citas = response.items;
        this.totalCitas = response.total;
        this.paginaActual = response.page;
        this.tamanioPagina = response.page_size;
        this.totalPaginas = Math.ceil(this.totalCitas / this.tamanioPagina);
        this.cargandoCitas.set(false);
        console.log('Citas cargadas:', response);
      },
      error: (err) => {
        console.error('Error al cargar citas:', err);
        this.notificationService.error('Error al cargar citas');
        this.cargandoCitas.set(false);
      }
    });
  }

  nuevaCita(): void {
    this.citaEnEdicion = null;
    this.form.reset({
      estado_id: 1,  // PROGRAMADA
      es_reposicion: 0
    });
    this.mostrarModal.set(true);
  }

  cerrarModal(): void {
    this.mostrarModal.set(false);
  }

  editarCita(cita: Cita): void {
    this.citaEnEdicion = cita;
    this.form.patchValue({
      nino_id: cita.nino_id,
      terapeuta_id: cita.terapeuta_id,
      terapia_id: cita.terapia_id,
      fecha: cita.fecha,
      hora_inicio: cita.hora_inicio,
      hora_fin: cita.hora_fin,
      estado_id: cita.estado_id,
      motivo: cita.motivo || '',
      observaciones: cita.observaciones || '',
      es_reposicion: cita.es_reposicion
    });
    this.mostrarModal.set(true);
  }

  enviarFormulario(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      this.notificationService.warning('Por favor completa todos los campos requeridos');
      return;
    }

    this.guardando.set(true);

    const formData = this.form.getRawValue();

    if (this.citaEnEdicion) {
      // Actualizar
      const citaUpdate: CitaUpdate = {
        nino_id: formData.nino_id,
        terapeuta_id: formData.terapeuta_id,
        terapia_id: formData.terapia_id,
        fecha: formData.fecha,
        hora_inicio: formData.hora_inicio,
        hora_fin: formData.hora_fin,
        estado_id: formData.estado_id,
        motivo: formData.motivo,
        observaciones: formData.observaciones,
        es_reposicion: formData.es_reposicion
      };

      this.citasService.updateCita(this.citaEnEdicion.id_cita, citaUpdate).subscribe({
        next: () => {
          this.guardando.set(false);
          this.notificationService.success('Cita actualizada correctamente');
          this.cerrarModal();
          this.cargarCitas();
        },
        error: (err) => {
          console.error('Error al actualizar cita:', err);
          this.guardando.set(false);
          this.notificationService.error('Error al actualizar cita');
        }
      });
    } else {
      // Crear
      const citaCreate: CitaCreate = {
        nino_id: formData.nino_id,
        terapeuta_id: formData.terapeuta_id,
        terapia_id: formData.terapia_id,
        fecha: formData.fecha,
        hora_inicio: formData.hora_inicio,
        hora_fin: formData.hora_fin,
        estado_id: formData.estado_id || 1,
        motivo: formData.motivo,
        observaciones: formData.observaciones,
        es_reposicion: formData.es_reposicion || 0
      };

      this.citasService.createCita(citaCreate).subscribe({
        next: () => {
          this.guardando.set(false);
          this.notificationService.success('Cita creada correctamente');
          this.cerrarModal();
          this.cargarCitas();
        },
        error: (err) => {
          console.error('Error al crear cita:', err);
          this.guardando.set(false);
          this.notificationService.error('Error al crear cita');
        }
      });
    }
  }

  aplicarFiltros(): void {
    this.paginaActual = 1;  // Reset a página 1 al aplicar filtros
    this.cargarCitas();
  }

  limpiarFiltros(): void {
    this.filtroFecha = '';
    this.filtroEstado = '';
    this.filtroBuscar = '';
    this.paginaActual = 1;
    this.cargarCitas();
  }

  cambiarEstado(cita: Cita, nuevoEstadoId: number): void {
    const estadoNombre = this.estadosCita.find(e => e.id === nuevoEstadoId)?.nombre || 'este estado';
    
    if (!confirm(`¿Cambiar estado de la cita a ${estadoNombre}?`)) {
      return;
    }

    this.citasService.cambiarEstado(cita.id_cita, nuevoEstadoId).subscribe({
      next: (citaActualizada) => {
        const index = this.citas.findIndex(c => c.id_cita === cita.id_cita);
        if (index !== -1) {
          this.citas[index] = citaActualizada;
        }
        this.notificationService.success('Estado actualizado correctamente');
      },
      error: (err) => {
        console.error('Error al cambiar estado:', err);
        this.notificationService.error('Error al cambiar estado');
      }
    });
  }

  eliminarCita(cita: Cita): void {
    if (!confirm('¿Estás seguro de eliminar esta cita?')) {
      return;
    }

    this.citasService.deleteCita(cita.id_cita).subscribe({
      next: () => {
        this.notificationService.success('Cita eliminada correctamente');
        this.cargarCitas();
      },
      error: (err) => {
        console.error('Error al eliminar cita:', err);
        this.notificationService.error('Error al eliminar cita');
      }
    });
  }

  cambiarPagina(pagina: number): void {
    if (pagina < 1 || pagina > this.totalPaginas) {
      return;
    }
    this.paginaActual = pagina;
    this.cargarCitas();
  }

  getEstadoNombre(estadoId: number): string {
    return this.estadosCita.find(e => e.id === estadoId)?.nombre || 'Desconocido';
  }

  getEstadoClase(estadoId: number): string {
    const codigo = this.estadosCita.find(e => e.id === estadoId)?.codigo || '';
    switch (codigo) {
      case 'PROGRAMADA':
        return 'badge-programada';
      case 'REALIZADA':
        return 'badge-realizada';
      case 'CANCELADA':
        return 'badge-cancelada';
      default:
        return 'badge-default';
    }
  }
}



