import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';

import { TerapeutaAgendaService, AccionResultado } from '../../service/terapeuta-agenda.service';
import { SesionTerapia } from '../../interfaces/horario-terapeuta.interface';

@Component({
  selector: 'app-horarios',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './horarios.html',
  styleUrls: ['./horarios.scss']
})
export class HorariosComponent implements OnInit {

  cargando = signal<boolean>(true);
  sesiones = signal<SesionTerapia[]>([]);
  vista = signal<'lista' | 'agenda'>('agenda');

  mensajeAccion = signal<string | null>(null);
  advertencias = signal<string[]>([]);

  horas = ['08:00','09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00'];
  diasSemana = [
    { num: 1, label: 'Lun' },
    { num: 2, label: 'Mar' },
    { num: 3, label: 'Mié' },
    { num: 4, label: 'Jue' },
    { num: 5, label: 'Vie' },
    { num: 6, label: 'Sáb' }
  ];

  sesionesOrdenadas = computed(() =>
    [...this.sesiones()].sort((a, b) => a.diaSemana - b.diaSemana || a.horaInicio.localeCompare(b.horaInicio))
  );

  constructor(private agendaService: TerapeutaAgendaService) {}

  ngOnInit(): void {
    this.cargarSesiones();
  }

  cambiarVista(v: 'lista' | 'agenda') {
    this.vista.set(v);
  }

  cargarSesiones() {
    this.cargando.set(true);
    this.mensajeAccion.set(null);
    this.advertencias.set([]);

    this.agendaService.getSesionesSemana().subscribe({
      next: (resp) => {
        this.sesiones.set(resp);
        this.cargando.set(false);
      },
      error: () => {
        this.cargando.set(false);
        this.mensajeAccion.set('No se pudieron cargar los horarios.');
      }
    });
  }

  sesionesEnSlot(diaNum: number, hora: string): SesionTerapia[] {
    return this.sesiones().filter(s =>
      s.diaSemana === diaNum && s.horaInicio === hora
    );
  }

  marcarCompletada(sesion: SesionTerapia) {
    this.mensajeAccion.set(null);
    this.advertencias.set([]);

    this.agendaService.marcarSesionCompletada(sesion.id).subscribe({
      next: (r: AccionResultado) => {
        this.mensajeAccion.set(r.mensaje);
        this.advertencias.set(r.advertencias ?? []);
        this.cargarSesiones(); // recarga estados desde la BD
      },
      error: () => {
        this.mensajeAccion.set('No se pudo marcar la sesión como completada.');
      }
    });
  }
}
