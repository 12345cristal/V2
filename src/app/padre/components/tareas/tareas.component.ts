import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardComponent } from '../shared/card/card.component';

interface Tarea {
  id: string;
  titulo: string;
  descripcion: string;
  fechaAsignacion: Date;
  fechaVencimiento: Date;
  estado: 'pendiente' | 'realizada' | 'vencida';
  terapeuta: string;
  objetivo: string;
  recursos: string[];
  instrucciones: string;
  completada: boolean;
}

@Component({
  selector: 'app-tareas',
  standalone: true,
  imports: [CommonModule, CardComponent],
  templateUrl: './tareas.component.html',
  styleUrls: ['./tareas.component.scss'],
})
export class TareasComponent implements OnInit {
  tareas: Tarea[] = [];
  filtroEstado: 'todas' | 'pendiente' | 'realizada' | 'vencida' = 'todas';
  
  ngOnInit() {
    this.cargarTareas();
  }
  
  private cargarTareas() {
    const hoy = new Date();
    const manana = new Date(hoy);
    manana.setDate(hoy.getDate() + 1);
    const ayer = new Date(hoy);
    ayer.setDate(hoy.getDate() - 1);
    
    this.tareas = [
      {
        id: '1',
        titulo: 'Ejercicios de articulación',
        descripcion: 'Practicar sonidos consonánticos frente al espejo',
        fechaAsignacion: new Date(hoy.getTime() - 2 * 24 * 60 * 60 * 1000),
        fechaVencimiento: hoy,
        estado: 'pendiente',
        terapeuta: 'Dra. María García',
        objetivo: 'Mejorar articulación de consonantes',
        recursos: ['Espejo', 'Tarjetas de imágenes'],
        instrucciones: 'Realizar 3 sesiones de 15 minutos durante el día. Enfocarse en los sonidos /r/ y /l/.',
        completada: false
      },
      {
        id: '2',
        titulo: 'Actividad sensorial con plastilina',
        descripcion: 'Hacer figuras simples con plastilina',
        fechaAsignacion: hoy,
        fechaVencimiento: manana,
        estado: 'pendiente',
        terapeuta: 'Dr. Carlos Ruiz',
        objetivo: 'Desarrollar motricidad fina',
        recursos: ['Plastilina de colores', 'Moldes'],
        instrucciones: 'Hacer 5 figuras diferentes. Empezar con formas simples como círculos y cuadrados.',
        completada: false
      },
      {
        id: '3',
        titulo: 'Lectura de cuento ilustrado',
        descripcion: 'Leer y comentar un cuento',
        fechaAsignacion: ayer,
        fechaVencimiento: ayer,
        estado: 'realizada',
        terapeuta: 'Dra. María García',
        objetivo: 'Comprensión lectora y expresión',
        recursos: ['Libro de cuentos'],
        instrucciones: 'Leer el cuento y hacer preguntas sobre los personajes.',
        completada: true
      }
    ];
    
    this.actualizarEstados();
  }
  
  get tareasFiltradas(): Tarea[] {
    if (this.filtroEstado === 'todas') {
      return this.tareas;
    }
    return this.tareas.filter(t => t.estado === this.filtroEstado);
  }
  
  get contadores() {
    return {
      total: this.tareas.length,
      pendientes: this.tareas.filter(t => t.estado === 'pendiente').length,
      realizadas: this.tareas.filter(t => t.estado === 'realizada').length,
      vencidas: this.tareas.filter(t => t.estado === 'vencida').length
    };
  }
  
  cambiarFiltro(estado: 'todas' | 'pendiente' | 'realizada' | 'vencida') {
    this.filtroEstado = estado;
  }
  
  toggleTarea(tarea: Tarea) {
    tarea.completada = !tarea.completada;
    if (tarea.completada) {
      tarea.estado = 'realizada';
    } else {
      this.actualizarEstados();
    }
  }
  
  private actualizarEstados() {
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);
    
    this.tareas.forEach(tarea => {
      if (!tarea.completada) {
        const vencimiento = new Date(tarea.fechaVencimiento);
        vencimiento.setHours(0, 0, 0, 0);
        
        if (vencimiento < hoy) {
          tarea.estado = 'vencida';
        } else {
          tarea.estado = 'pendiente';
        }
      }
    });
  }
}
