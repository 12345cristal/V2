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
  imports: [
    CommonModule,
    HeaderComponent,
    FooterComponent,
    ChatbotIaComponent
  ],
  templateUrl: './landing.html',
  styleUrls: ['./landing.scss']
})
export class LandingPageComponent {

  /** Imagen principal del hero */
  heroImageUrl: string = 'nina-terapia.png';

  constructor(private router: Router) {}

 
  scrollToServices(): void {
    const section =
      document.getElementById('services') ||
      document.getElementById('therapies');

    if (section) {
      section.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  }

  /**
   * Navega al login del sistema
   */
  goToLogin(): void {
    this.router.navigate(['/login']);
  }
}

