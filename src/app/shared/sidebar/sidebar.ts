import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './sidebar.html',
  styleUrls: ['./sidebar.scss'],
})
export class Sidebar implements OnInit {

  @Input() open: boolean = false;
  @Output() closeSidebar = new EventEmitter<void>();

  userName: string = 'Usuario';
  roleName: string = '';
  
  // Flags para mostrar/ocultar menús
  isCoordinador: boolean = false;
  isTerapeuta: boolean = false;
  isPadre: boolean = false;

  constructor(private auth: AuthService) {}

  ngOnInit() {
    const user = this.auth.user;
    const rolId = user?.rol_id ?? null;

    // Configurar nombre de usuario
    this.userName = user ? `${user.nombres} ${user.apellido_paterno}` : 'Usuario';
    this.roleName = this.getRoleDisplayName(rolId);

    // Activar el menú correspondiente al rol
    this.isCoordinador = rolId === 1 || rolId === 2;
    this.isTerapeuta = rolId === 3;
    this.isPadre = rolId === 4;
  }

  getRoleDisplayName(roleId: number | null): string {
    const roles: Record<number, string> = {
      1: 'Administrador',
      2: 'Coordinador',
      3: 'Terapeuta',
      4: 'Padre/Tutor'
    };
    return roles[roleId!] || 'Usuario';
  }

  close() {
    this.closeSidebar.emit();
  }

  logout() {
    this.auth.logout();
  }
}
