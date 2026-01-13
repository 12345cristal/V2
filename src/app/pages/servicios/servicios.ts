import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FooterComponent } from "../../shared/footer/footer";
import { HeaderComponent } from "../../shared/header/header";
import { ChatbotIaComponent } from '../../shared/chatbot-ia/chatbot-ia.component';

@Component({
  selector: 'app-servicios',
  standalone: true,
  imports: [CommonModule, FooterComponent, HeaderComponent, ChatbotIaComponent],
  template: `
    <app-header></app-header>

    <section class="servicios-container">

      <!-- Encabezado principal -->
      <div class="section-header">
        <h1>Nuestros Servicios</h1>
        <h2>Atención Integral para el Desarrollo</h2>
      </div>

      <!-- descripción general -->
      <p>
        En Autismo Mochis IAP ofrecemos terapias y programas especializados para apoyar el desarrollo integral de niños y jóvenes con Trastorno del Espectro Autista (TEA).
        Nuestro equipo profesional diseña intervenciones personalizadas para promover autonomía, comunicación e inclusión social.
      </p>

      <!-- Lista de servicios -->
      <div class="servicios-grid">

        <!-- Terapia de Lenguaje -->
        <div class="servicio-card">
          <img src="/servicios/lenguaje.jpeg" alt="Terapia de Lenguaje" class="servicio-img">
          <h3>Terapia de Lenguaje</h3>
          <p>
            Potencia la comunicación verbal, no verbal y habilidades sociales mediante estrategias adaptadas al nivel de desarrollo del niño.
          </p>
        </div>

        <!-- Terapia Física / Fisioterapia -->
        <div class="servicio-card">
          <img src="/servicios/fisioterapia.jpeg" alt="Terapia Física" class="servicio-img">
          <h3>Fisioterapia</h3>
          <p>
            Mejora el control postural, tono muscular, fuerza, equilibrio y coordinación a través de ejercicios especializados.
          </p>
        </div>

        <!-- Neuromotor -->
        <div class="servicio-card">
          <img src="/servicios/neuromotor.jpeg" alt="Terapia Neuromotora" class="servicio-img">
          <h3>Terapia Neuromotora</h3>
          <p>
            Fortalece la integración sensorial y la conexión neuromuscular para favorecer movimiento funcional y autonomía.
          </p>
        </div>

        <!-- Psicopedagogía -->
        <div class="servicio-card">
          <img src="/servicios/psicopedagogia.jpeg" alt="Psicopedagogía" class="servicio-img">
          <h3>Psicopedagogía</h3>
          <p>
            Apoyo en aprendizaje, atención, memoria, lectura-escritura y habilidades académicas esenciales.
          </p>
        </div>

        <!-- Psicología Conductual -->
        <div class="servicio-card">
          <img src="/servicios/psicologia-infantil.jpg" alt="Psicología Conductual" class="servicio-img">
          <h3>Psicología Conductual</h3>
          <p>
            Estrategias conductuales centradas en fortalecer habilidades sociales, emocionales y de autorregulación para mejorar el bienestar del niño.
          </p>
        </div>

        <!-- Capacitaciones -->
        <div class="servicio-card">
          <img src="/servicios/capacitacion.jpg" alt="Capacitaciones y Talleres" class="servicio-img">
          <h3>Capacitaciones y Talleres</h3>
          <p>
            Cursos dirigidos a padres, docentes y terapeutas sobre estrategias inclusivas, manejo del TEA y comunicación efectiva.
          </p>
        </div>

      </div>

      <!-- CTA -->
      <div class="cta">
        <p>Trabajamos con compromiso, empatía y profesionalismo para transformar vidas.</p>
        <button class="contact-button">Agenda tu Cita</button>
      </div>

    </section>

    <app-chatbot-ia></app-chatbot-ia>
    <app-footer></app-footer>
  `,
  styleUrls: ['./servicios.scss']
})
export class ServiciosComponent {}



