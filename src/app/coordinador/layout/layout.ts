import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Toolbar } from '../../share/toolbar/toolbar';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [RouterOutlet, Toolbar],
  templateUrl: './layout.html',
  styleUrl: './layout.scss',
})
export class Layout {}
