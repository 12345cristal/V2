import { Component, signal } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-perfil-menu',
  standalone: true,
  templateUrl: './perfil-menu.html',
  styleUrls: ['./perfil-menu.scss']
})
export class PerfilMenuComponent {

  fotoPerfil = signal('assets/img/user.jpg');

  constructor(private router: Router) {}

  irPerfil() {
    this.router.navigate(['/perfil']);
  }

  cerrarSesion() {
    localStorage.clear();
    this.router.navigate(['/login']);
  }
}
