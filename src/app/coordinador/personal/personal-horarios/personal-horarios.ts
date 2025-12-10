import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';

import { Personal, HorarioPersonal } from '../../../interfaces/personal.interface';
import { PersonalService } from '../../../service/personal.service';

@Component({
  selector: 'app-personal-horarios',
  standalone: true,
  templateUrl: './personal-horarios.html',
  styleUrls: ['./personal-horarios.scss'],
  imports: [CommonModule, MatIconModule, FormsModule]
})
export class PersonalHorariosComponent implements OnInit {

  personal?: Personal;
  cargando = true;
  mostrarFormulario = false;
  editando = false;

  dias = ['', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];

  horarioForm: HorarioPersonal = {
    dia_semana: 1,
    hora_inicio: '09:00',
    hora_fin: '17:00'
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private personalService: PersonalService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.cargarDatos(id);
  }

  cargarDatos(id: number): void {
    this.cargando = true;
    this.personalService.getPersonalById(id).subscribe({
      next: p => {
        this.personal = p;
        this.cargando = false;
      },
      error: () => this.cargando = false
    });
  }

  volver(): void {
    this.router.navigate(['/coordinador/personal']);
  }

  abrirFormulario(): void {
    this.mostrarFormulario = true;
    this.editando = false;
    this.horarioForm = {
      dia_semana: 1,
      hora_inicio: '09:00',
      hora_fin: '17:00'
    };
  }

  cerrarFormulario(): void {
    this.mostrarFormulario = false;
    this.editando = false;
  }

  editarHorario(horario: HorarioPersonal): void {
    this.mostrarFormulario = true;
    this.editando = true;
    this.horarioForm = { ...horario };
  }

  guardarHorario(): void {
    if (!this.personal?.id_personal) return;

    if (!this.horarioForm.dia_semana || !this.horarioForm.hora_inicio || !this.horarioForm.hora_fin) {
      alert('Completa todos los campos');
      return;
    }

    if (this.horarioForm.hora_inicio >= this.horarioForm.hora_fin) {
      alert('La hora de inicio debe ser menor que la hora de fin');
      return;
    }

    const horarioData = {
      ...this.horarioForm,
      id_personal: this.personal.id_personal
    };

    if (this.editando && this.horarioForm.id_horario) {
      // Actualizar
      this.personalService.updateHorario(this.horarioForm.id_horario, horarioData).subscribe({
        next: () => {
          this.cargarDatos(this.personal!.id_personal!);
          this.cerrarFormulario();
        },
        error: (err) => {
          alert(err.error?.detail || 'Error al actualizar horario');
        }
      });
    } else {
      // Crear
      this.personalService.createHorario(horarioData).subscribe({
        next: () => {
          this.cargarDatos(this.personal!.id_personal!);
          this.cerrarFormulario();
        },
        error: (err) => {
          alert(err.error?.detail || 'Error al crear horario. Puede que se solape con otro horario existente.');
        }
      });
    }
  }

  eliminarHorario(horario: HorarioPersonal): void {
    if (!horario.id_horario) return;

    const dia = this.dias[horario.dia_semana];
    if (!confirm(`¿Eliminar horario del ${dia} de ${horario.hora_inicio} a ${horario.hora_fin}?`)) {
      return;
    }

    this.personalService.deleteHorario(horario.id_horario).subscribe({
      next: () => {
        this.cargarDatos(this.personal!.id_personal!);
      },
      error: () => {
        alert('Error al eliminar horario');
      }
    });
  }

}
