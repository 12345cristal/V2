import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

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

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.scss'],
})
export class InicioComponent implements OnInit {
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
      weekday: 'long',
      day: 'numeric',
      month: 'long',
    });
  }
}
