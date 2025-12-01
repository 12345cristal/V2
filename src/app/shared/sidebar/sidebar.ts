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
  @Input() rol: string = '';
  @Output() closeSidebar = new EventEmitter<void>();

  menu: any[] = [];

  ngOnInit() {
    this.loadMenuByRole();
  }

  loadMenuByRole() {

    // ----------- COORDINADOR -----------
    if (this.rol === 'coordinador') {
      this.menu = [
        { label: 'Citas', route: '/coordinador/citas', icon: 'event' },
        { label: 'Personal', route: '/coordinador/personal', icon: 'group' },
        { label: 'Niños Beneficiados', route: '/coordinador/ninos', icon: 'child_care' },
        { label: 'Usuarios', route: '/coordinador/usuarios', icon: 'manage_accounts' },
        { label: 'Terapias', route: '/coordinador/terapias', icon: 'medication' },
        { label: 'Perfil', route: '/coordinador/perfil', icon: 'account_circle' },
        { label: 'Configuración', route: '/coordinador/configuracion', icon: 'settings' },
      ];
    }

    // ----------- TERAPEUTA -----------
    if (this.rol === 'terapeuta') {
      this.menu = [
        { label: 'Inicio', route: '/terapeuta/inicio', icon: 'home' },
        { label: 'Pacientes', route: '/terapeuta/pacientes', icon: 'group' },
        { label: 'Horarios', route: '/terapeuta/horarios', icon: 'schedule' },
        { label: 'Recursos', route: '/terapeuta/recursos', icon: 'assignment' },
        { label: 'Perfil', route: '/terapeuta/perfil', icon: 'account_circle' },
      ];
    }

    // ----------- PADRE -----------
    // ----------- PADRE -----------
if (this.rol === 'padre') {
  this.menu = [
    { label: 'Inicio', route: '/padre/inicio', icon: 'home' },

    { label: 'Información del niño', route: '/padre/info-nino', icon: 'child_care' },

    { label: 'Actividades', route: '/padre/actividades', icon: 'checklist' },

    { label: 'Progreso', route: '/padre/progreso', icon: 'timeline' },

    { label: 'Terapias', route: '/padre/terapias', icon: 'event' },

    { label: 'Documentos', route: '/padre/documentos', icon: 'folder' },

    { label: 'Pagos', route: '/padre/pagos', icon: 'payments' },

    { label: 'Perfil', route: '/padre/perfil', icon: 'account_circle' },
  ];
}

  }
}
