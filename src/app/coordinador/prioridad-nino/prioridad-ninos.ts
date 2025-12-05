import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DecisionSupportService } from '../../service/decision-support.service';

@Component({
  selector: 'app-prioridad-ninos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './prioridad-ninos.html',
  styleUrls: ['./prioridad-ninos.scss']
})
export class PrioridadNinosComponent implements OnInit {

  resultados: any[] = [];
  cargando = false;
  error = '';

  // Pesos por defecto
  pesos = {
    max_resultados: 10,
    peso_prioridad: 0.4,
    peso_tiempo_espera: 0.3,
    peso_asistencias: 0.15,
    peso_inasistencias: 0.15,
  };

  constructor(private decisionSupport: DecisionSupportService) {}

  ngOnInit(): void {
    this.calcular();
  }

  calcular(): void {
    this.cargando = true;
    this.error = '';

    this.decisionSupport.calcularPrioridad(this.pesos).subscribe({
      next: (res: any[]) => {
        this.resultados = res;
        this.cargando = false;
      },
      error: () => {
        this.error = 'No se pudo calcular prioridad.';
        this.cargando = false;
      },
    });
  }

  descargarPdf(): void {
    this.decisionSupport.descargarPdfPrioridad(this.pesos).subscribe({
      next: (archivo: Blob) => {
        const url = window.URL.createObjectURL(archivo);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'prioridad_ninos.pdf';
        a.click();
        window.URL.revokeObjectURL(url);
      },
      error: () => {
        this.error = 'No se pudo descargar el PDF.';
      },
    });
  }
}
