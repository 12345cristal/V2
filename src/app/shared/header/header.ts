import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './header.html',
  styleUrls: ['./header.scss']
})
export class HeaderComponent {
  menuAbierto = false;

  toggleMenu() {
    this.menuAbierto = !this.menuAbierto;

    const boton = document.querySelector('.menu-toggle');
    if (boton) {
      boton.classList.toggle('active', this.menuAbierto);
    }

    if (this.menuAbierto) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }
  }

  cerrarMenu() {
    this.menuAbierto = false;

    const boton = document.querySelector('.menu-toggle');
    if (boton) boton.classList.remove('active');

    document.body.style.overflow = "auto";
  }
}

