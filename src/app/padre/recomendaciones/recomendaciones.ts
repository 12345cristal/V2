import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecomendacionService, RecursoRecomendado } from '../../service/recomendacion.service';

@Component({
  selector: 'app-recomendaciones-padre',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './recomendaciones.html',
  styleUrls: ['./recomendaciones.scss']
})
export class RecomendacionesPadreComponent implements OnInit {

  recomendaciones: RecursoRecomendado[] = [];
  cargando = false;
  error = '';
  idNino = 0;

  constructor(private recomendacionService: RecomendacionService) {}

  ngOnInit() {
    this.idNino = Number(localStorage.getItem('id_nino_activo'));
    this.obtener();
  }

  obtener() {
    this.cargando = true;
    this.error = '';

    this.recomendacionService.obtenerRecomendaciones(this.idNino).subscribe({
      next: (res: RecursoRecomendado[]) => {
        this.recomendaciones = res;
        this.cargando = false;
      },
      error: (err: any) => {
        console.error(err);
        this.error = 'No se pudieron cargar las recomendaciones';
        this.cargando = false;
      }
    });
  }
}
