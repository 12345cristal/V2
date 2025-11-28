import { Component, Input, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TerapeutaPacientesService } from '../../services/terapeuta-pacientes.service';
import { BitacoraEntrada } from '../../interfaces/bitacora.interface';

@Component({
  selector: 'app-bitacora-historial',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './bitacora-historial.html',
  styleUrls: ['./bitacora-historial.scss']
})
export class BitacoraHistorialComponent implements OnInit {

  @Input() pacienteId!: number;

  cargando = signal<boolean>(true);
  historial = signal<BitacoraEntrada[]>([]);

  constructor(private service: TerapeutaPacientesService) {}

  ngOnInit(): void {
    this.cargar();
  }

  cargar() {
    this.cargando.set(true);

    this.service.getHistorialBitacora(this.pacienteId).subscribe({
      next: (resp) => {
        this.historial.set(resp);
        this.cargando.set(false);
      },
      error: () => this.cargando.set(false)
    });
  }
}
