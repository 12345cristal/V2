import { Component, OnInit } from '@angular/core';
import { TherapyService } from '../../service/terapias.service';
import { TerapeutaRecomendado } from '../../interfaces/terapeuta-recomendado.interface';

@Component({
  selector: 'app-recomendacion-terapeutas',
  templateUrl: './recomendar-terapeutas.html',
  styleUrls: ['./recomendar-terapeutas.scss'],
})
export class RecomendacionTerapeutas implements OnInit {

  // Hasta 3 terapeutas fijos
  terapeuta1: TerapeutaRecomendado | null = null;
  terapeuta2: TerapeutaRecomendado | null = null;
  terapeuta3: TerapeutaRecomendado | null = null;

  cargando = false;
  error = '';
  mostrarModal = false;
  terapeutaSeleccionado: TerapeutaRecomendado | null = null;

  constructor(private terapiasService: TherapyService) {}

  ngOnInit(): void {
    this.obtenerRecomendaciones();
  }

  obtenerRecomendaciones(): void {
    this.cargando = true;
    this.error = '';
    this.terapeuta1 = this.terapeuta2 = this.terapeuta3 = null;

    const payload = {}; // Ajusta según tus criterios

    this.terapiasService.recomendarTerapeutas(payload).subscribe({
      next: (res: TerapeutaRecomendado[]) => {
        if (res[0]) this.terapeuta1 = this.convertirNumeros(res[0]);
        if (res[1]) this.terapeuta2 = this.convertirNumeros(res[1]);
        if (res[2]) this.terapeuta3 = this.convertirNumeros(res[2]);
        this.cargando = false;
      },
      error: (err: any) => {
        console.error(err);
        this.error = 'No se pudieron obtener las recomendaciones';
        this.cargando = false;
      }
    });
  }

  abrirModal(terapeuta: TerapeutaRecomendado): void {
    this.terapeutaSeleccionado = terapeuta;
    this.mostrarModal = true;
  }

  cerrarModal(): void {
    this.terapeutaSeleccionado = null;
    this.mostrarModal = false;
  }

  asignar(): void {
    if (!this.terapeutaSeleccionado) return;

    const { id_personal, id_terapia } = this.terapeutaSeleccionado;

    this.terapiasService.asignarTerapia(id_personal, id_terapia).subscribe({
      next: () => {
        alert(`Terapeuta ${this.terapeutaSeleccionado?.nombre_completo} asignado correctamente`);
        this.cerrarModal();
        this.obtenerRecomendaciones();
      },
      error: (err: any) => {
        console.error(err);
        alert('Error al asignar el terapeuta');
      }
    });
  }

  private convertirNumeros(t: TerapeutaRecomendado): TerapeutaRecomendado {
    return {
      ...t,
      score: Number(t.score),
      criterios: {
        rating: Number(t.criterios.rating),
        carga: Number(t.criterios.carga),
        sesiones: Number(t.criterios.sesiones),
        afinidad: Number(t.criterios.afinidad)
      }
    };
  }
}



