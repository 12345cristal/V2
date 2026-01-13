import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { CoordinadorPersonalService } from '../../service/coordinador-personal.service';
import { TerapeutaCargaDetalle } from '../../interfaces/terapeuta-detalle.interface';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Component({
  selector: 'app-terapeuta-detalle',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './terapeuta-detalle.html',
  styleUrls: ['./terapeuta-detalle.scss']
})
export class TerapeutaDetalleComponent implements OnInit {

  terapeuta: TerapeutaCargaDetalle | null = null;
  cargando = false;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private coordService: CoordinadorPersonalService
  ) {}

  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');
    const id = idParam ? Number(idParam) : 0;
    if (!id) {
      this.error = 'ID inválido';
      return;
    }
    this.cargarDetalle(id);
  }

  cargarDetalle(id: number): void {
    this.cargando = true;
    this.error = '';

    this.coordService.getDetalleTerapeuta(id)
      .pipe(
        catchError((err) => {
          console.error(err);
          this.error = 'No se pudo cargar el detalle.';
          this.cargando = false;
          return of(null); // Evita que falle el subscribe
        })
      )
      .subscribe((detalle) => {
        if (detalle) {
          this.terapeuta = detalle;
        }
        this.cargando = false;
      });
  }

  getDiaLabel(dia: number): string {
    const dias = ['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'];
    return dias[dia - 1] ?? '';
  }
}

