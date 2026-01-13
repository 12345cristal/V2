import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './sidebar.html',
  styleUrls: ['./sidebar.scss'],
})// src/app/shared/sidebar/sidebar.ts
export class Sidebar implements OnInit {

  @Input() open = false;
    @Input() rol: number | null = null; // ✅ OBLIGATORIO para layout
  @Output() closeSidebar = new EventEmitter<void>();

  userName = 'Usuario';
  roleName = '';

  isCoordinador = false;
  isTerapeuta = false;
  isPadre = false;

  constructor(private auth: AuthService) {}

  ngOnInit(): void {
    const user = this.auth.user();

    if (user) {
      this.userName = `${user.nombres} ${user.apellido_paterno}`;
      this.roleName = this.getRoleDisplayName(user.rol_id);

      this.isCoordinador = user.rol_id === 1 || user.rol_id === 2;
      this.isTerapeuta = user.rol_id === 3;
      this.isPadre = user.rol_id === 4;
    }
  }

  getRoleDisplayName(roleId: number): string {
    return {
      1: 'Administrador',
      2: 'Coordinador',
      3: 'Terapeuta',
      4: 'Padre/Tutor'
    }[roleId] ?? 'Usuario';
  }

  close(): void {
    this.closeSidebar.emit();
  }

  logout(): void {
    this.auth.logout();
  }
}
