import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { TopsisService } from '../../service/topsis.service';
import { TopsisRequest, TopsisResultado } from '../../interfaces/topsis.interface';

@Component({
  selector: 'app-topsis-terapeutas',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './topsis-terapeutas.html',
  styleUrls: ['./topsis-terapeutas.scss']
})
export class TopsisTerapeutasComponent {

  pesos = {
    carga: 0.4,
    sesiones: 0.3,
    rating: 0.3
  };

  criterios = ["carga", "sesiones", "rating"];
  tipo = ["costo", "costo", "beneficio"];

  matriz: number[][] = [];

  resultados: TopsisResultado[] = [];

  constructor(private topsisSrv: TopsisService) {}

  generarMatrizEjemplo() {
    this.matriz = [
      [10, 4, 4.5],
      [8, 3, 4.8],
      [12, 5, 4.1]
    ];
  }

  calcular() {
    const body: TopsisRequest = {
      criterios: this.criterios,
      matriz: this.matriz,
      pesos: [this.pesos.carga, this.pesos.sesiones, this.pesos.rating],
      tipo_criterio: this.tipo as any,
      top_k: 3
    };

    this.topsisSrv.calcularPersonalizado(body).subscribe(res => {
      this.resultados = res;
    });
  }
}
