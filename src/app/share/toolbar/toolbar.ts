import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-toolbar',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './toolbar.html',
  styleUrl: './toolbar.scss',
})
export class Toolbar {
  menuAbierto = false;

  toggleUserMenu() {
    this.menuAbierto = !this.menuAbierto;
  }
}
