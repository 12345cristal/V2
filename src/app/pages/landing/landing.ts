// src/app/pages/landing/landing.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { HeaderComponent } from '../../shared/header/header';
import { FooterComponent } from '../../shared/footer/footer';
import { ChatbotIaComponent } from '../../shared/chatbot-ia/chatbot-ia.component';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule, HeaderComponent, FooterComponent, ChatbotIaComponent],
  template: `
    <!-- src/app/pages/landing/landing.html -->

    <app-header></app-header>

    <main class="landing-container">

      <!-- HERO -->
      <section class="hero-section">
        <div class="hero-content">

          <!-- Texto -->
          <div class="text-section">
            <h1 class="title">
              Transformando <br />
              <span class="line">Vidas con</span>
              <span class="highlight">Amor y Ciencia</span>
            </h1>

            <p class="subtitle">
              En AUTISMO MOCHIS creemos en el potencial único de cada persona.
              Brindamos servicios especializados para el desarrollo integral
              de personas con autismo y apoyo a sus familias.
            </p>

            <!-- Botones -->
            <div class="buttons">
              <button class="btn-primary" (click)="scrollToServices()">
                Conoce nuestros servicios
              </button>

              <button class="btn-outline" (click)="goToLogin()">
                Ingresar al sistema
              </button>
            </div>

            <!-- Stats -->
            <div class="stats">
              <div class="stat">
                <h3>150+</h3>
                <p>Familias beneficiadas</p>
              </div>
              <div class="stat">
                <h3>10+</h3>
                <p>Terapeutas especializados</p>
              </div>
              <div class="stat">
                <h3>10</h3>
                <p>Años de experiencia</p>
              </div>
              <div class="stat">
                <h3>30+</h3>
                <p>Niños en terapia</p>
              </div>
            </div>
          </div>

          <!-- Imagen -->
          <div class="image-section">
            <img [src]="heroImageUrl" alt="Niña en terapia" />
          </div>

        </div>
      </section>

      <!-- POR QUÉ ELEGIRNOS -->
      <section class="why-section">
        <div class="container">
          <h2>¿Por qué elegirnos?</h2>
          <p>
            Combinamos experiencia profesional con un enfoque humano y tecnología
            de vanguardia para ofrecer el mejor cuidado posible.
          </p>

          <div class="features">
            <article class="feature">
              <h3>Equipo multidisciplinario</h3>
              <p>
                Terapia de lenguaje, psicología, psicopedagogía, neuromotor
                y fisioterapia en un solo lugar.
              </p>
            </article>

            <article class="feature">
              <h3>Resultados comprobados</h3>
              <p>
                Más de 150 familias han visto avances significativos en sus hijos
                gracias a nuestros programas.
              </p>
            </article>

            <article class="feature">
              <h3>Seguimiento continuo</h3>
              <p>
                Reportes claros y comunicación constante entre terapeutas
                y familias.
              </p>
            </article>
          </div>
        </div>
      </section>

      <!-- TERAPIAS -->
      <section class="therapies-section">
        <div class="container">
          <h2>Nuestras terapias</h2>

          <div class="therapies-cards">
            <article class="therapy-card">
              <div class="icon">🗣️</div>
              <h3>Terapia de lenguaje</h3>
              <p>Desarrollo de habilidades comunicativas y expresión verbal.</p>
            </article>

            <article class="therapy-card">
              <div class="icon">🧠</div>
              <h3>Psicología infantil</h3>
              <p>Apoyo emocional, social y conductual para niñas y niños.</p>
            </article>

            <article class="therapy-card">
              <div class="icon">📚</div>
              <h3>Psicopedagogía</h3>
              <p>Estrategias de aprendizaje y adaptación escolar.</p>
            </article>

            <article class="therapy-card">
              <div class="icon">🏃‍♂️</div>
              <h3>Terapia neuromotor</h3>
              <p>Estimulación motora, coordinación y equilibrio.</p>
            </article>

            <article class="therapy-card">
              <div class="icon">💪</div>
              <h3>Fisioterapia</h3>
              <p>Mejora de fuerza, movilidad y control postural.</p>
            </article>
          </div>
        </div>
      </section>

    </main>

    <app-chatbot-ia></app-chatbot-ia>
    <app-footer></app-footer>
  `,
  styleUrls: ['./landing.scss']
})
export class LandingPageComponent {

  heroImageUrl = 'niña_terapia.png';

  constructor(private router: Router) {}

  scrollToServices(): void {
    // Si luego pones un id="servicios" en otra sección, puedes usar scrollIntoView
    window.scrollTo({ top: 800, behavior: 'smooth' });
  }

  goToLogin(): void {
    this.router.navigate(['/login']);
  }
}
