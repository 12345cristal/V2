import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { TherapyService } from '../../service/terapias.service';
import { Terapia } from '../../interfaces/terapia.interfaz';
import { NotificationService } from '../../shared/notification.service';

@Component({
  selector: 'app-terapias',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './terapias.html',
  styleUrls: ['./terapias.scss']
})
export class TerapiasComponent implements OnInit {

  terapias: Terapia[] = [];
  personalDisponible: any[] = [];
  personalAsignado: any[] = [];

  form!: FormGroup;
  modoEdicion: boolean = false;
  terapiaSeleccionada: Terapia | null = null;

  mostrarModal: boolean = false;

  constructor(
    private terapiaService: TherapyService,
    private fb: FormBuilder,
    private notificationService: NotificationService
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.cargarDatos();
  }

  cargarDatos() {
    this.terapiaService.getTerapias().subscribe({
      next: (res) => {
        console.log('Terapias cargadas:', res);
        this.terapias = res;
      },
      error: (err) => {
        console.error('Error al cargar terapias:', err);
        this.notificationService.error('No se pudieron cargar las terapias');
      }
    });

    this.terapiaService.getPersonalDisponible().subscribe({
      next: (res) => {
        console.log('Personal disponible:', res);
        this.personalDisponible = res as any[];
      },
      error: (err) => console.error('Error al cargar personal disponible:', err)
    });

    this.terapiaService.getPersonalAsignado().subscribe({
      next: (res) => {
        console.log('Personal asignado:', res);
        this.personalAsignado = res as any[];
      },
      error: (err) => console.error('Error al cargar personal asignado:', err)
    });
  }

  initForm() {
    this.form = this.fb.group({
      nombre: ['', Validators.required],
      descripcion: ['']
    });
  }

  abrirCrear() {
    this.modoEdicion = false;
    this.terapiaSeleccionada = null;
    this.form.reset();
    this.mostrarModal = true;
  }

  abrirEditar(terapia: Terapia) {
    this.modoEdicion = true;
    this.terapiaSeleccionada = terapia;

    this.form.patchValue({
      nombre: terapia.nombre,
      descripcion: terapia.descripcion
    });

    this.mostrarModal = true;
  }

  cerrarModal() {
    this.mostrarModal = false;
  }

guardar() {
  if (this.form.invalid) {
    this.notificationService.warning('Por favor, llena todos los campos obligatorios.');
    this.form.markAllAsTouched();
    return;
  }

  const data = this.form.value;

  if (this.modoEdicion && this.terapiaSeleccionada) {
    this.terapiaService.actualizarTerapia(
      this.terapiaSeleccionada.id_terapia!,
      data
    ).subscribe({
      next: () => {
        this.cargarDatos();
        this.cerrarModal();
        this.notificationService.success('Terapia actualizada correctamente');
      },
      error: () => {
        this.notificationService.error('No se pudo actualizar la terapia');
      }
    });

  } else {
    this.terapiaService.crearTerapia(data).subscribe({
      next: () => {
        this.cargarDatos();
        this.cerrarModal();
        this.notificationService.success('Terapia creada correctamente');
      },
      error: () => {
        this.notificationService.error('No se pudo crear la terapia');
      }
    });
  }
}


  cambiarEstado(terapia: Terapia) {
    console.log('Cambiando estado de terapia:', terapia);
    
    const nuevoEstado = terapia.estado === 'ACTIVA' ? 'INACTIVA' : 'ACTIVA';
    const accion = nuevoEstado === 'ACTIVA' ? 'activar' : 'inactivar';
    
    if (!confirm(`¿Estás seguro de ${accion} la terapia "${terapia.nombre}"?`)) {
      console.log('Usuario canceló el cambio de estado');
      return;
    }

    console.log('Llamando al servicio para cambiar estado. ID:', terapia.id_terapia);
    
    this.terapiaService.cambiarEstado(terapia.id_terapia!).subscribe({
      next: (terapiaActualizada) => {
        console.log('Respuesta del servidor:', terapiaActualizada);
        // Actualizar el estado localmente
        terapia.estado = terapiaActualizada.estado;
        this.notificationService.success(`Terapia ${terapiaActualizada.estado.toLowerCase()} correctamente`);
      },
      error: (err) => {
        console.error('Error al cambiar estado:', err);
        console.error('Status:', err.status);
        console.error('Message:', err.message);
        this.notificationService.error('No se pudo cambiar el estado de la terapia');
      }
    });
  }

  asignar(id_personal: number, id_terapia: number) {
    if (!id_terapia || id_terapia === 0) {
      this.notificationService.warning('Debes seleccionar una terapia');
      return;
    }

    this.terapiaService.asignarPersonal({ id_personal, id_terapia }).subscribe({
      next: () => {
        this.cargarDatos();
        this.notificationService.success('Terapeuta asignado correctamente');
      },
      error: () => {
        this.notificationService.error('No se pudo asignar el terapeuta');
      }
    });
  }

  toNumber(value: string): number {
    return parseInt(value, 10);
  }
}
