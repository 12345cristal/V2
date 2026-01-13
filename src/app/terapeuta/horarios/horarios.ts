import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HorarioService } from '../../service/terapeuta/horario.service';

type EventoHorario = {
  dia_semana: number;     // 1=Lunes ... 7=Domingo
  hora_inicio: string;    // HH:mm:ss
  hora_fin: string;
  nino_nombre: string;
  terapia_nombre: string;
};

@Component({
  standalone: true,
  selector: 'app-horario',
  imports: [CommonModule],
  templateUrl: './horarios.html',
  styleUrls: ['./horarios.scss'],
})
export class HorarioPage {
  dias = [
    { id: 1, nombre: 'Lunes' },
    { id: 2, nombre: 'Martes' },
    { id: 3, nombre: 'Miércoles' },
    { id: 4, nombre: 'Jueves' },
    { id: 5, nombre: 'Viernes' },
    { id: 6, nombre: 'Sábado' },
    { id: 7, nombre: 'Domingo' },
  ];

  eventos: EventoHorario[] = [];
  cargando = true;

  constructor(private horarioService: HorarioService) {
    this.horarioService.getHorarioSemanal().subscribe({
      next: data => (this.eventos = data),
      complete: () => (this.cargando = false),
    });
  }

  eventosPorDia(dia: number) {
    return this.eventos.filter(e => e.dia_semana === dia);
  }
}
