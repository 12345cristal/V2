import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
<<<<<<< Updated upstream
import { InicioService } from '../services/inicio.service';
import { InicioPadre } from '../interfaces/inicio.interface';
=======

interface ResumenNino {
  id: string;
  nombre: string;
  proximaSesion: {
    fecha: Date;
    hora: string;
    terapeuta: string;
    tipo: string;
  };
  ultimoAvance: {
    fecha: Date;
    descripcion: string;
    porcentaje: number;
  };
  pagosPendientes: number;
  documentoNuevo: boolean;
  ultimaObservacion: {
    fecha: Date;
    terapeuta: string;
    resumen: string;
  };
}
>>>>>>> Stashed changes

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.scss'],
})
export class InicioComponent implements OnInit {
<<<<<<< Updated upstream

  saludo = '';
  data!: InicioPadre;
  cargando = true;

  constructor(private inicioService: InicioService) {}

  ngOnInit(): void {
    this.generarSaludo();
    this.cargarInicio();
  }

  private generarSaludo(): void {
    const hora = new Date().getHours();
    if (hora < 12) this.saludo = 'Buenos días';
    else if (hora < 18) this.saludo = 'Buenas tardes';
    else this.saludo = 'Buenas noches';
  }

  cargarInicio(hijoId?: string): void {
    this.cargando = true;

    this.inicioService.obtenerInicio(hijoId).subscribe({
      next: res => {
        this.data = res;
        this.cargando = false;
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  formatearFecha(fecha: string): string {
    return new Date(fecha).toLocaleDateString('es-MX', {
=======
  resumen: ResumenNino | null = null;
  saludo: string = '';
  horaActual: number = 0;

  ngOnInit() {
    this.generarSaludo();
    this.cargarResumen();
  }

  private generarSaludo() {
    this.horaActual = new Date().getHours();
    if (this.horaActual < 12) {
      this.saludo = 'Buenos días';
    } else if (this.horaActual < 18) {
      this.saludo = 'Buenas tardes';
    } else {
      this.saludo = 'Buenas noches';
    }
  }

  private cargarResumen() {
    this.resumen = {
      id: '1',
      nombre: 'Juan Pérez',
      proximaSesion: {
        fecha: new Date(Date.now() + 86400000),
        hora: '10:00 AM',
        terapeuta: 'Dra. María García',
        tipo: 'Logopedia',
      },
      ultimoAvance: {
        fecha: new Date(),
        descripcion: 'Mejora en socialización',
        porcentaje: 75,
      },
      pagosPendientes: 500000,
      documentoNuevo: true,
      ultimaObservacion: {
        fecha: new Date(),
        terapeuta: 'Dra. María García',
        resumen:
          'El niño mostró buena disposición en la sesión de hoy. Continuar con ejercicios en casa.',
      },
    };
  }

  obtenerFechaFormato(fecha: Date): string {
    return fecha.toLocaleDateString('es-CO', {
>>>>>>> Stashed changes
      weekday: 'long',
      day: 'numeric',
      month: 'long',
    });
  }
}
