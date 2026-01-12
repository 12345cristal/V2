import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CardComponent } from '../shared/card/card.component';

interface Recurso {
  id: string;
  titulo: string;
  descripcion: string;
  tipo: 'pdf' | 'video' | 'enlace' | 'imagen';
  url: string;
  terapeuta: string;
  objetivo: string;
  fechaSubida: Date;
  thumbnail?: string;
}

@Component({
  selector: 'app-recursos',
  standalone: true,
  imports: [CommonModule, FormsModule, CardComponent],
  templateUrl: './recursos.component.html',
  styleUrls: ['./recursos.component.scss'],
})
export class RecursosComponent implements OnInit {
  recursos: Recurso[] = [];
  filtroTipo: string = 'todos';
  filtroTerapeuta: string = 'todos';
  terapeutas: string[] = [];
  
  ngOnInit() {
    this.cargarRecursos();
    this.extraerTerapeutas();
  }
  
  private cargarRecursos() {
    this.recursos = [
      {
        id: '1',
        titulo: 'Guía de ejercicios de articulación',
        descripcion: 'Ejercicios prácticos para mejorar la articulación de sonidos',
        tipo: 'pdf',
        url: '/recursos/guia-articulacion.pdf',
        terapeuta: 'Dra. María García',
        objetivo: 'Mejora de articulación',
        fechaSubida: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
      },
      {
        id: '2',
        titulo: 'Video: Actividades sensoriales en casa',
        descripcion: 'Aprende a realizar actividades sensoriales con materiales caseros',
        tipo: 'video',
        url: 'https://youtube.com/watch?v=example',
        terapeuta: 'Dr. Carlos Ruiz',
        objetivo: 'Estimulación sensorial',
        fechaSubida: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000),
        thumbnail: '/assets/video-thumbnail.jpg'
      },
      {
        id: '3',
        titulo: 'Recursos de comunicación visual',
        descripcion: 'Colección de pictogramas y tarjetas de comunicación',
        tipo: 'enlace',
        url: 'https://example.com/pictogramas',
        terapeuta: 'Dra. María García',
        objetivo: 'Comunicación alternativa',
        fechaSubida: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000)
      }
    ];
  }
  
  private extraerTerapeutas() {
    this.terapeutas = [...new Set(this.recursos.map(r => r.terapeuta))];
  }
  
  get recursosFiltrados(): Recurso[] {
    return this.recursos.filter(recurso => {
      const coincideTipo = this.filtroTipo === 'todos' || recurso.tipo === this.filtroTipo;
      const coincideTerapeuta = this.filtroTerapeuta === 'todos' || recurso.terapeuta === this.filtroTerapeuta;
      return coincideTipo && coincideTerapeuta;
    });
  }
  
  getIconoTipo(tipo: string): string {
    switch (tipo) {
      case 'pdf': return 'fas fa-file-pdf';
      case 'video': return 'fas fa-video';
      case 'enlace': return 'fas fa-link';
      case 'imagen': return 'fas fa-image';
      default: return 'fas fa-file';
    }
  }
  
  getColorTipo(tipo: string): string {
    switch (tipo) {
      case 'pdf': return '#e74c3c';
      case 'video': return '#9b59b6';
      case 'enlace': return '#3498db';
      case 'imagen': return '#2ecc71';
      default: return '#95a5a6';
    }
  }
  
  abrirRecurso(recurso: Recurso) {
    window.open(recurso.url, '_blank');
  }
}
