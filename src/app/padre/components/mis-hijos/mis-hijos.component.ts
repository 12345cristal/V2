import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardComponent } from '../shared/card/card.component';

interface Hijo {
  id: string;
  nombre: string;
  edad: number;
  foto: string;
  diagnostico: string;
  fechaDiagnostico: Date;
  medicamentos: Medicamento[];
  alergias: string[];
  terapeuta: string;
  proximaSesion: Date;
}

interface Medicamento {
  nombre: string;
  dosis: string;
  frecuencia: string;
  horarios: string[];
}

@Component({
  selector: 'app-mis-hijos',
  standalone: true,
  imports: [CommonModule, CardComponent],
  templateUrl: './mis-hijos.component.html',
  styleUrls: ['./mis-hijos.component.scss'],
})
export class MisHijosComponent implements OnInit {
  hijos: Hijo[] = [];
  hijoSeleccionado?: Hijo;
  
  ngOnInit() {
    this.cargarHijos();
  }
  
  private cargarHijos() {
    // Mock data - en producción esto vendría de un servicio
    this.hijos = [
      {
        id: '1',
        nombre: 'Juan Pérez',
        edad: 8,
        foto: '/assets/default-avatar.png',
        diagnostico: 'Trastorno del Espectro Autista (TEA) - Nivel 2',
        fechaDiagnostico: new Date(2020, 3, 15),
        medicamentos: [
          {
            nombre: 'Risperidona',
            dosis: '0.5mg',
            frecuencia: 'Cada 12 horas',
            horarios: ['08:00 AM', '08:00 PM']
          },
          {
            nombre: 'Melatonina',
            dosis: '3mg',
            frecuencia: 'Una vez al día',
            horarios: ['09:00 PM']
          }
        ],
        alergias: ['Penicilina', 'Maní', 'Látex'],
        terapeuta: 'Dra. María García',
        proximaSesion: new Date(Date.now() + 86400000)
      }
    ];
    
    if (this.hijos.length > 0) {
      this.hijoSeleccionado = this.hijos[0];
    }
  }
  
  seleccionarHijo(hijo: Hijo) {
    this.hijoSeleccionado = hijo;
  }
  
  calcularEdad(fechaNacimiento: Date): number {
    const hoy = new Date();
    const edad = hoy.getFullYear() - fechaNacimiento.getFullYear();
    return edad;
  }
}
