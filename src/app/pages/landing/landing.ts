// src/app/pages/landing/landing.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { HeaderComponent } from '../../shared/header/header';
import { FooterComponent } from '../../shared/footer/footer';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [CommonModule, HeaderComponent, FooterComponent],
  templateUrl: './landing.html',
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
