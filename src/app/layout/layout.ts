import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { Toolbar } from '../share/toolbar/toolbar';
import { Sidebar } from '../coordinador/sidebar/sidebar';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [RouterOutlet, Toolbar, Sidebar],
  templateUrl: './layout.html',
  styleUrl: './layout.scss',
})
export class Layout {
  sidebarOpen = false;

  toggleSidebar() {
    this.sidebarOpen = !this.sidebarOpen;
  }
}
