import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HorarioService } from '../../service/terapeuta/horario.service';
import { EventoHorario } from '../../interfaces/terapeuta/evento-horario.interface';

@Component({
  standalone: true,
  selector: 'app-horario',
  imports: [CommonModule],
  templateUrl: './horarios.html',
  styleUrls: ['./horarios.scss'],
})
export class HorarioPage implements OnInit {

  dias = [
    { id: 1, nombre: 'Lunes' },
    { id: 2, nombre: 'Martes' },
    { id: 3, nombre: 'Miércoles' },
    { id: 4, nombre: 'Jueves' },
    { id: 5, nombre: 'Viernes' },

  ];

  eventos: EventoHorario[] = [];
  cargando = true;

  constructor(private horarioService: HorarioService) {}

  ngOnInit(): void {
    this.horarioService.getHorarioSemanal().subscribe({
      next: data => {
        this.eventos = data;
        this.cargando = false;
      },
      error: err => {
        console.error(err);
        this.cargando = false;
      }
    });
  }

  eventosPorDia(dia: number): EventoHorario[] {
    return this.eventos.filter(e => e.dia_semana === dia);
  }
}
