import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { Toolbar } from '../toolbar/toolbar';
import { Sidebar } from '../sidebar/sidebar';
import { AuthService } from '../../service/auth.service';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [RouterOutlet, Toolbar, Sidebar],
  templateUrl: './layout.html',
  styleUrl: './layout.scss',
})
export class Layout {

  sidebarOpen = false;
  rolUsuario = '';

  constructor(private auth: AuthService) {}

  ngOnInit() {
    this.rolUsuario = this.auth.getRol();
  }

  toggleSidebar() {
    this.sidebarOpen = !this.sidebarOpen;
  }
}
