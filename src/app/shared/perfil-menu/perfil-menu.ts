import { Component, signal, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-perfil-menu',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './perfil-menu.html',
  styleUrls: ['./perfil-menu.scss']
})
export class PerfilMenuComponent implements OnInit {

  fotoPerfil = signal<string>('assets/img/user.jpg');

  constructor(private router: Router) {}

  ngOnInit(): void {
    this.cargarFotoPerfil();
  }

  private cargarFotoPerfil(): void {
    // Obtener foto de perfil del usuario actual
    const usuarioStr = localStorage.getItem('usuario');
    if (usuarioStr) {
      try {
        const usuario = JSON.parse(usuarioStr);
        if (usuario.foto_perfil) {
          this.fotoPerfil.set(usuario.foto_perfil);
        }
      } catch (e) {
        console.error('Error al parsear usuario:', e);
      }
    }
  }

  irPerfil(): void {
    // Navegar a la ruta de perfil según el rol
    const rol = localStorage.getItem('rol');
    
    switch(rol) {
      case 'COORDINADOR':
        this.router.navigate(['/coordinador/perfil']);
        break;
      case 'TERAPEUTA':
        this.router.navigate(['/terapeuta/perfil']);
        break;
      case 'PADRE':
        this.router.navigate(['/padre/perfil']);
        break;
      default:
        this.router.navigate(['/perfil']);
    }
  }

  cerrarSesion(): void {
    if (confirm('¿Estás seguro que deseas cerrar sesión?')) {
      localStorage.removeItem('token');
      localStorage.removeItem('usuario');
      localStorage.removeItem('rol');
      localStorage.removeItem('foto_perfil');
      localStorage.removeItem('rol');
      localStorage.removeItem('foto_perfil');
      
      // Redirigir al login
      this.router.navigate(['/login']);
    }
  }
}
