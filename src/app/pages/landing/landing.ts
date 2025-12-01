import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../../shared/header/header';
import { FooterComponent } from '../../shared/footer/footer';
import { Router } from '@angular/router';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule, HeaderComponent, FooterComponent],
  templateUrl: './landing.html',
  styleUrls: ['./landing.scss']
})
export class LandingPageComponent {

  // Imagen hero local
  heroImageUrl = 'tera/nina_ent.jpg';

  constructor(private router: Router) {}

  // Botones principales
  data = {
    button1: {
      text: 'Conoce nuestros servicios',
      action: () => window.scrollTo({ top: 800, behavior: 'smooth' })
    },
    button2: {
      text: 'Ingresar al sistema',
      action: () => this.router.navigate(['/login'])
    }
  };

  // Estadísticas
  stats = [
    { count: '150+', label: 'Familias beneficiadas', color: '#3b82f6' },
    { count: '10+', label: 'Terapeutas especializados', color: '#10b981' },
    { count: '10', label: 'Años de experiencia', color: '#f59e0b' },
    { count: '30+', label: 'Niños en terapia', color: '#f43f5e' }
  ];

  // Terapias ofrecidas
  therapies = [
    {
      name: 'Terapia de Lenguaje',
      description: 'Desarrollo de habilidades comunicativas y expresión verbal.',
      icon: '🗣️'
    },
    {
      name: 'Psicología Infantil',
      description: 'Apoyo emocional, social y conductual.',
      icon: '🧠'
    },
    {
      name: 'Psicopedagogía',
      description: 'Estrategias de aprendizaje y adaptación escolar.',
      icon: '📚'
    },
    {
      name: 'Terapia Neuromotor',
      description: 'Estimulación motora fina y gruesa, coordinación y equilibrio.',
      icon: '🏃‍♂️'
    },
    {
      name: 'Fisioterapia',
      description: 'Mejora de fuerza, movilidad y control postural.',
      icon: '💪'
    }
  ];
}
