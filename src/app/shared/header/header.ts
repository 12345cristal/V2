import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'; // Esto permite usar routerLink

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule], // ⚡ Importante agregar RouterModule
  templateUrl: './header.html',
  styleUrls: ['./header.scss']
})
export class HeaderComponent {
  menuAbierto = false;

  toggleMenu() {
    this.menuAbierto = !this.menuAbierto;
    const btn = document.querySelector('.menu-toggle');
    if (btn) {
      btn.classList.toggle('active', this.menuAbierto);
    }
  }

  cerrarMenu() {
    this.menuAbierto = false;
  }
}
