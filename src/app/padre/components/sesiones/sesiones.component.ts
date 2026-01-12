import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardComponent } from '../shared/card/card.component';
import { ModalComponent } from '../shared/modal/modal.component';

interface Sesion {
  id: string;
  fecha: Date;
  hora: string;
  terapeuta: string;
  tipo: string;
  estado: 'programada' | 'realizada' | 'cancelada';
  duracion: number;
  observaciones?: string;
  objetivos?: string[];
  recursos?: string[];
}

@Component({
  selector: 'app-sesiones',
  standalone: true,
  imports: [CommonModule, CardComponent, ModalComponent],
  templateUrl: './sesiones.component.html',
  styleUrls: ['./sesiones.component.scss'],
})
export class SesionesComponent implements OnInit {
  sesiones: Sesion[] = [];
  tabActiva: 'hoy' | 'programadas' | 'semana' = 'hoy';
  sesionSeleccionada?: Sesion;
  mostrarModal: boolean = false;
  
  ngOnInit() {
    this.cargarSesiones();
  }
  
  private cargarSesiones() {
    const hoy = new Date();
    const manana = new Date(hoy);
    manana.setDate(hoy.getDate() + 1);
    
    this.sesiones = [
      {
        id: '1',
        fecha: hoy,
        hora: '10:00 AM',
        terapeuta: 'Dra. María García',
        tipo: 'Logopedia',
        estado: 'programada',
        duracion: 60,
        objetivos: ['Mejorar articulación', 'Ejercicios de respiración'],
        recursos: ['Tarjetas de vocabulario', 'Espejo']
      },
      {
        id: '2',
        fecha: manana,
        hora: '3:00 PM',
        terapeuta: 'Dr. Carlos Ruiz',
        tipo: 'Terapia Ocupacional',
        estado: 'programada',
        duracion: 45,
        objetivos: ['Coordinación motriz fina', 'Actividades sensoriales']
      },
      {
        id: '3',
        fecha: new Date(hoy.getTime() - 2 * 24 * 60 * 60 * 1000),
        hora: '11:00 AM',
        terapeuta: 'Dra. María García',
        tipo: 'Logopedia',
        estado: 'realizada',
        duracion: 60,
        observaciones: 'Excelente sesión. El niño mostró gran avance en la articulación de consonantes.',
        objetivos: ['Sonidos consonánticos', 'Comprensión verbal']
      }
    ];
  }
  
  get sesionesFiltradas(): Sesion[] {
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);
    
    switch (this.tabActiva) {
      case 'hoy':
        return this.sesiones.filter(s => {
          const fecha = new Date(s.fecha);
          fecha.setHours(0, 0, 0, 0);
          return fecha.getTime() === hoy.getTime();
        });
      
      case 'programadas':
        return this.sesiones.filter(s => s.estado === 'programada');
      
      case 'semana':
        const unaSemana = new Date(hoy.getTime() + 7 * 24 * 60 * 60 * 1000);
        return this.sesiones.filter(s => {
          const fecha = new Date(s.fecha);
          return fecha >= hoy && fecha <= unaSemana;
        });
      
      default:
        return this.sesiones;
    }
  }
  
  cambiarTab(tab: 'hoy' | 'programadas' | 'semana') {
    this.tabActiva = tab;
  }
  
  verDetalle(sesion: Sesion) {
    this.sesionSeleccionada = sesion;
    this.mostrarModal = true;
  }
  
  cerrarModal() {
    this.mostrarModal = false;
    this.sesionSeleccionada = undefined;
  }
  
  getEstadoClass(estado: string): string {
    switch (estado) {
      case 'programada':
        return 'badge-info';
      case 'realizada':
        return 'badge-success';
      case 'cancelada':
        return 'badge-error';
      default:
        return 'badge';
    }
  }
  
  getEstadoLabel(estado: string): string {
    switch (estado) {
      case 'programada':
        return 'Programada';
      case 'realizada':
        return 'Realizada';
      case 'cancelada':
        return 'Cancelada';
      default:
        return estado;
    }
  }
}
