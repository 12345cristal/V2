import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

import { AuthService } from '../../auth/auth.service';

// IMPORTA tus componentes standalone
import { Toolbar } from '../toolbar/toolbar';
import { Sidebar } from '../sidebar/sidebar';
import { ChatbotIaComponent } from '../chatbot-ia/chatbot-ia.component';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    Toolbar,
    Sidebar,
    ChatbotIaComponent
  ],
  templateUrl: './layout.html',
  styleUrls: ['./layout.scss']
})// src/app/shared/layout/layout.ts
export class LayoutComponent {

  sidebarOpen = false;
  rolUsuario: number | null = null;

  constructor(private auth: AuthService) {
    const user = this.auth.user();
    this.rolUsuario = user?.rol_id ?? null;
  }

  toggleSidebar(): void {
    this.sidebarOpen = !this.sidebarOpen;
  }
}
