import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecursosService } from '../../service/terapeuta/recursos.service'; 
import { Recurso } from '../../interfaces/terapeuta/recurso.interface';

@Component({
  standalone: true,
  selector: 'app-recursos',
  imports: [CommonModule],
  templateUrl: './recursos-terapeuta.html',
  styleUrls: ['./recursos-terapeuta.scss'],
})
export class RecursosPage {
  recursos: Recurso[] = [];

  constructor(private recursosService: RecursosService) {
    this.recursosService.getRecursos().subscribe(r => (this.recursos = r));
  }
}
