import { Component, EventEmitter, Output } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-toolbar',
  standalone: true,
  imports: [MatIconModule],
  templateUrl: './toolbar.html',
  styleUrl: './toolbar.scss',
})
export class Toolbar {
  @Output() menuClick = new EventEmitter<void>();

  onMenuClick() {
    this.menuClick.emit(); // ❗ esto avisará al layout que abra/cierre el sidebar
  }
}
