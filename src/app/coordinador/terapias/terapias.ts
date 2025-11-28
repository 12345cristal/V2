import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

import { TherapyService } from '../../service/terapias.service';
import { Terapia } from '../../interfaces/terapia.interfaz';

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
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.cargarDatos();
  }

  cargarDatos() {
    this.terapiaService.getTerapias().subscribe(res => {
      this.terapias = res;
    });

    this.terapiaService.getPersonalDisponible().subscribe(res => {
      this.personalDisponible = res as any[];
    });

    this.terapiaService.getPersonalAsignado().subscribe(res => {
      this.personalAsignado = res as any[];
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
    this.mostrarError('Por favor, llena todos los campos obligatorios.');
    this.form.markAllAsTouched();
    return;
  }

  const data = this.form.value;

  if (this.modoEdicion && this.terapiaSeleccionada) {
    this.terapiaService.actualizarTerapia(
      this.terapiaSeleccionada.id_terapia!,
      data
    ).subscribe(() => {
      this.cargarDatos();
      this.cerrarModal();
      this.mostrarMensaje('Terapia actualizada correctamente');
    });

  } else {
    this.terapiaService.crearTerapia(data).subscribe(() => {
      this.cargarDatos();
      this.cerrarModal();
      this.mostrarMensaje('Terapia creada correctamente');
    });
  }
}


  cambiarEstado(terapia: Terapia) {
    this.terapiaService.cambiarEstado(terapia.id_terapia!)
      .subscribe(() => this.cargarDatos());
  }

  asignar(id_personal: number, id_terapia: number) {
    if (!id_terapia || id_terapia === 0) return;

    this.terapiaService.asignarPersonal({ id_personal, id_terapia })
      .subscribe(() => this.cargarDatos());
  }
  toNumber(value: string): number {
  return parseInt(value, 10);
}

mostrarMensaje(mensaje: string) {
  const div = document.createElement('div');
  div.className = 'toast-exito';
  div.innerText = mensaje;

  document.body.appendChild(div);

  setTimeout(() => {
    div.classList.add('show');
  }, 10);

  setTimeout(() => {
    div.classList.remove('show');
    setTimeout(() => div.remove(), 300);
  }, 2500);
}

mostrarError(mensaje: string) {
  const div = document.createElement('div');
  div.className = 'toast-error';
  div.innerText = mensaje;

  document.body.appendChild(div);

  setTimeout(() => {
    div.classList.add('show');
  }, 10);

  setTimeout(() => {
    div.classList.remove('show');
    setTimeout(() => div.remove(), 300);
  }, 2500);
}



}
