import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { InicioService } from '../../service/padres/inicio.service';
import { InicioPadre } from '../../interfaces/padres/inicio.interface';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.scss'],
})
export class InicioComponent implements OnInit {
  data: InicioPadre | null = null;
  cargando = false;
  error: string | null = null;

  // 1. Propiedad para el saludo
  saludo: string = '';

  // 2. Propiedad para el hijo seleccionado
  hijoSeleccionadoId: number | null = null;

  private inicioService = inject(InicioService);

  ngOnInit(): void {
    // Generar saludo basado en la hora
    const hora = new Date().getHours();
    if (hora < 12) {
      this.saludo = 'Buenos días';
    } else if (hora < 19) {
      this.saludo = 'Buenas tardes';
    } else {
      this.saludo = 'Buenas noches';
    }
    
    this.cargarInicio();
  }

  cargarInicio(hijoId?: string): void {
    this.cargando = true;
    this.error = null;

    this.inicioService.obtenerInicio(hijoId).subscribe({
      next: (res: InicioPadre) => {
        this.data = res;
        this.cargando = false;
      },
      error: (err: any) => {
        console.error('Error al cargar inicio:', err);
        this.error = 'Error al cargar los datos';
        this.cargando = false;
      }
    });
  }

  // 3. Método para cambiar hijo
  cambiarHijo(event: any): void {
    this.hijoSeleccionadoId = event;
    // Aquí puedes agregar lógica adicional para cargar datos del hijo seleccionado
    console.log('Hijo seleccionado:', this.hijoSeleccionadoId);
  }

  // 4. Método para formatear fecha
  formatearFecha(fecha: string | Date): string {
    if (!fecha) return '';
    
    const date = typeof fecha === 'string' ? new Date(fecha) : fecha;
    
    return date.toLocaleDateString('es-MX', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  }
}
