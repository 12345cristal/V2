import { Component, Input, Output, EventEmitter } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './sidebar.html',
  styleUrl: './sidebar.scss',
})
export class Sidebar {

  @Input() open = false;

  @Output() closeSidebar = new EventEmitter<void>();

  // 🔵 MENÚ DEL TERAPEUTA
  menu = [
    { label: 'Inicio', route: '/terapeuta/inicio', icon: 'home' },
    { label: 'Pacientes', route: '/terapeuta/pacientes', icon: 'group' },
    { label: 'Horarios', route: '/terapeuta/horarios', icon: 'schedule' },
    { label: 'Actividades', route: '/terapeuta/actividades', icon: 'assignment' },
    { label: 'Perfil', route: '/terapeuta/perfil', icon: 'account_circle' },
  ];
}
