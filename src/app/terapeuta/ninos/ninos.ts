import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NinosService } from '../../service/ninos.service';
import { Nino } from '../../interfaces/nino.interface';

@Component({
  standalone: true,
  selector: 'app-ninos-list',
  imports: [CommonModule, RouterModule],
  templateUrl: './ninos.html',
  styleUrls: ['./ninos.scss'],
})
export class NinosPage {
  ninos: Nino[] = [];

  constructor(private ninosService: NinosService) {
    this.cargar();
  }

  cargar() {
    this.ninosService.getNinos().subscribe({
      next: res => (this.ninos = res),
    });
  }
}
