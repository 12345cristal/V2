import { Component, Input, Output, EventEmitter } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../auth/auth.service';

interface MenuItem {
  label: string;
  route: string;
  icon: string;
  permiso?: string;
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './sidebar.html',
  styleUrls: ['./sidebar.scss'],
})
export class Sidebar {

  @Input() open: boolean = false;

  // Rol del usuario (coordinador, padre, terapeuta)
  @Input() rol: number | null = null;

  @Output() closeSidebar = new EventEmitter<void>();

  permisos: string[] = [];
  menu: MenuItem[] = [];

  constructor(private auth: AuthService) {}

  ngOnInit() {
    const user = this.auth.user;
    this.permisos = user?.permisos ?? [];
    this.loadMenu();
  }

  loadMenu() {
    const fullMenu: MenuItem[] = [

      // ==========================
      // 🟦 COORDINADOR
      // ==========================
      { label: 'Citas', route: '/coordinador/citas', icon: 'event', permiso: 'citas:ver' },
      { label: 'Personal', route: '/coordinador/personal', icon: 'group', permiso: 'personal:ver' },
      { label: 'Niños Beneficiados', route: '/coordinador/ninos', icon: 'child_care', permiso: 'ninos:ver' },
      { label: 'Usuarios', route: '/coordinador/usuarios', icon: 'manage_accounts', permiso: 'usuarios:ver' },
      { label: 'Terapias', route: '/coordinador/terapias', icon: 'medication', permiso: 'terapias:ver' },
      { label: 'Configuración', route: '/coordinador/configuracion', icon: 'settings', permiso: 'configuracion:ver' },
      { label: 'Ahuillo de Prioridad', route: '/coordinador/ahuillo-prioridad', icon: 'priority_high', permiso: 'prioridad:ver' },
      { label: 'Perfil', route: '/coordinador/perfil', icon: 'account_circle' },

      // ==========================
      // 🟩 TERAPEUTA
      // ==========================
      { label: 'Inicio', route: '/terapeuta/inicio', icon: 'home', permiso: 'inicio:ver' },
      { label: 'Pacientes', route: '/terapeuta/pacientes', icon: 'group', permiso: 'pacientes:ver' },
      { label: 'Horarios', route: '/terapeuta/horarios', icon: 'schedule', permiso: 'horarios:ver' },
      { label: 'Recursos', route: '/terapeuta/recursos', icon: 'assignment', permiso: 'recursos:ver' },
      { label: 'Perfil', route: '/terapeuta/perfil', icon: 'account_circle' },

      // ==========================
      // 🟨 PADRE
      // ==========================
      { label: 'Inicio', route: '/padre/inicio', icon: 'home', permiso: 'padre:ver' },
      { label: 'Información del niño', route: '/padre/info-nino', icon: 'child_care', permiso: 'info-nino:ver' },
      { label: 'Actividades', route: '/padre/actividades', icon: 'checklist', permiso: 'actividades:ver' },
      { label: 'Terapias', route: '/padre/terapias', icon: 'event', permiso: 'padre-terapias:ver' },
      { label: 'Documentos', route: '/padre/documentos', icon: 'folder', permiso: 'documentos:ver' },
      { label: 'Recomendaciones', route: '/padre/recomendaciones', icon: 'tips_and_updates', permiso: 'recomendaciones:ver' },
      { label: 'Perfil', route: '/padre/perfil', icon: 'account_circle' }
    ];

    // 🔍 FILTRO POR PERMISOS
    this.menu = fullMenu.filter(item =>
      !item.permiso || this.permisos.includes(item.permiso)
    );
  }
}
