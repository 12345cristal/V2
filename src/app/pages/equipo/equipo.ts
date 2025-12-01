import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../../shared/header/header';
import { FooterComponent } from '../../shared/footer/footer';

interface Terapeuta {
  nombre: string;
  cargo: string;
  descripcion: string;
  imagen: string;
}

@Component({
  selector: 'app-equipo',
  standalone: true,
  imports: [CommonModule, HeaderComponent, FooterComponent],
  templateUrl: './equipo.html',
  styleUrls: ['./equipo.scss']
})
export class Equipo {
  modalAbierto = false;
  terapeutaSeleccionado: Terapeuta | null = null;

  // Información de terapeutas
  terapeutas: Terapeuta[] = [
    {
      nombre: 'Lic. Ana Lucía',
      cargo: 'Neuromotor',
      descripcion: 'Se enfoca en el desarrollo de habilidades motoras, coordinación y motricidad fina y gruesa.',
      imagen: 'tera/neuro.jpg'
    },
    {
      nombre: 'Lic. Arisbet',
      cargo: 'Fisioterapia',
      descripcion: 'Ayuda a mejorar el control corporal, movilidad y postura, con ejercicios personalizados.',
      imagen: 'tera/fisio.jpg'
    },
    {
      nombre: 'Lic. Ariadna Soto Quiñonez',
      cargo: 'Psicopedagogía',
      descripcion: 'Especialista en estrategias de aprendizaje, desarrollo cognitivo y apoyo escolar.',
      imagen: 'tera/pedagogia.jpg'
    },
    {
      nombre: 'Lic. Jesus',
      cargo: 'Psicología',
      descripcion: 'Ofrecen apoyo emocional y acompañamiento psicológico a familias y pacientes.',
      imagen: 'tera/psico2.jpg'
    },
    {
      nombre: 'Lic. Rocio',
      cargo: 'Psicología',
      descripcion: 'Ofrecen apoyo emocional y acompañamiento psicológico a familias y pacientes.',
      imagen: 'tera/psico.jpg'
    },
    {
      nombre: 'Lic. Judith',
      cargo: 'Lenguaje',
      descripcion: 'Especialista en Terapia de Lenguaje para mejorar la comunicación verbal y no verbal.',
      imagen: 'tera/leng.jpg'
    }
  ];

  abrirModal(terapeuta: Terapeuta) {
    this.terapeutaSeleccionado = terapeuta;
    this.modalAbierto = true;
  }

  cerrarModal() {
    this.modalAbierto = false;
    this.terapeutaSeleccionado = null;
  }
}
