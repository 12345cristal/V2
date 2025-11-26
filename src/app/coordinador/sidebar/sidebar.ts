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

  // 👇 ESTE OUTPUT ES CLAVE
  @Output() closeSidebar = new EventEmitter<void>();

  menu = [
    { label: 'Citas', route: '/coordinador/citas', icon: 'event' },
    { label: 'Personal', route: '/coordinador/personal', icon: 'group' },
    { label: 'Niños Beneficiados', route: '/coordinador/ninos', icon: 'child_care' },
    { label: 'Usuarios', route: '/coordinador/usuarios', icon: 'manage_accounts' },
    { label: 'Terapias', route: '/coordinador/terapias', icon: 'medication' },
    { label: 'Perfil', route: '/coordinador/perfil', icon: 'account_circle' },
    { label: 'Configuración', route: '/coordinador/configuracion', icon: 'settings' },
  ];
}
