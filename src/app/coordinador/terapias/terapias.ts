import { Component, OnInit, signal, computed, inject, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';

import { TherapyService } from '../../service/terapias.service';
import { Terapia } from '../../interfaces/terapia.interfaz';
import { NotificationService } from '../../shared/notification.service';

@Component({
  selector: 'app-terapias',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatIconModule],
  templateUrl: './terapias.html',
  styleUrl: './terapias.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class TerapiasComponent implements OnInit {

  readonly terapias = signal<Terapia[]>([]);
  readonly personalDisponible = signal<any[]>([]);
  readonly personalAsignado = signal<any[]>([]);
  readonly form = signal<FormGroup | null>(null);
  readonly modoEdicion = signal(false);
  readonly terapiaSeleccionada = signal<Terapia | null>(null);
  readonly mostrarModal = signal(false);
  readonly mostrarConfirmEstado = signal(false);
  readonly cargando = signal(false);
  readonly filtroSexo = signal<'todos' | 'M' | 'F'>('todos');
  readonly filtroTerapia = signal<number | 'todos'>('todos');
  readonly busqueda = signal('');

  private terapiaService = inject(TherapyService);
  private fb = inject(FormBuilder);
  private notificationService = inject(NotificationService);

  readonly personalAsignadoFiltrado = computed(() => {
    let personal = this.personalAsignado();
    const sexo = this.filtroSexo();
    const terapia = this.filtroTerapia();
    const busqueda = this.busqueda().toLowerCase();

    if (sexo !== 'todos') {
      personal = personal.filter(p => p.sexo === sexo);
    }

    if (terapia !== 'todos') {
      personal = personal.filter(p => p.id_terapia === terapia);
    }

    if (busqueda) {
      personal = personal.filter(p => 
        p.nombre_completo?.toLowerCase().includes(busqueda) || false
      );
    }

    return personal;
  });

  ngOnInit(): void {
    this.form.set(this.fb.group({
      nombre: ['', Validators.required],
      descripcion: ['']
    }));
    this.cargarDatos();
  }

  cargarDatos(): void {
    this.cargando.set(true);

    this.terapiaService.getTerapias().subscribe({
      next: (res) => {
        this.terapias.set(res);
      },
      error: (err) => {
        console.error('Error al cargar terapias:', err);
        this.notificationService.error('No se pudieron cargar las terapias');
      }
    });

    this.terapiaService.getPersonalDisponible().subscribe({
      next: (res) => {
        this.personalDisponible.set(res as any[]);
      },
      error: (err) => console.error('Error al cargar personal disponible:', err),
      complete: () => this.cargando.set(false)
    });

    this.terapiaService.getPersonalAsignado().subscribe({
      next: (res) => {
        this.personalAsignado.set(res as any[]);
      },
      error: (err) => console.error('Error al cargar personal asignado:', err)
    });
  }

  abrirCrear(): void {
    this.modoEdicion.set(false);
    this.terapiaSeleccionada.set(null);
    const f = this.form();
    if (f) {
      f.reset();
    }
    this.mostrarModal.set(true);
  }

  abrirEditar(terapia: Terapia): void {
    this.modoEdicion.set(true);
    this.terapiaSeleccionada.set(terapia);
    const f = this.form();
    if (f) {
      f.patchValue({
        nombre: terapia.nombre,
        descripcion: terapia.descripcion
      });
    }
    this.mostrarModal.set(true);
  }

  cerrarModal(): void {
    this.mostrarModal.set(false);
  }

  guardar(): void {
    const f = this.form();
    if (!f || f.invalid) {
      this.notificationService.warning('Por favor, completa los campos obligatorios');
      return;
    }

    const datos = f.value;
    const terapia = this.terapiaSeleccionada();

    if (this.modoEdicion() && terapia) {
      this.terapiaService.actualizarTerapia(terapia.id_terapia!, datos).subscribe({
        next: () => {
          this.notificationService.success('Terapia actualizada correctamente');
          this.cerrarModal();
          this.cargarDatos();
        },
        error: () => this.notificationService.error('Error al actualizar la terapia')
      });
    } else {
      this.terapiaService.crearTerapia(datos).subscribe({
        next: () => {
          this.notificationService.success('Terapia creada correctamente');
          this.cerrarModal();
          this.cargarDatos();
        },
        error: () => this.notificationService.error('Error al crear la terapia')
      });
    }
  }

  abrirConfirmEstado(terapia: Terapia): void {
    this.terapiaSeleccionada.set(terapia);
    this.mostrarConfirmEstado.set(true);
  }

  cerrarConfirmEstado(): void {
    this.mostrarConfirmEstado.set(false);
    this.terapiaSeleccionada.set(null);
  }

  confirmarCambioEstado(): void {
    const terapia = this.terapiaSeleccionada();
    if (!terapia) return;

    this.terapiaService.cambiarEstado(terapia.id_terapia!).subscribe({
      next: (terapiaActualizada) => {
        terapia.estado = terapiaActualizada.estado;
        this.notificationService.success(`Terapia ${terapiaActualizada.estado.toLowerCase()} correctamente`);
        this.cerrarConfirmEstado();
      },
      error: () => {
        this.notificationService.error('No se pudo cambiar el estado de la terapia');
      }
    });
  }

  asignar(id_personal: number, id_terapia: number): void {
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

