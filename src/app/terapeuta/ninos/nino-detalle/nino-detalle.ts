import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { NinosService } from '../../../service/ninos.service';
import { Nino } from '../../../interfaces/nino.interface';

@Component({
  standalone: true,
  selector: 'app-nino-detalle',
  imports: [CommonModule, RouterModule],
  templateUrl: './nino-detalle.html',
  styleUrls: ['./nino-detalle.scss'],
})
export class NinoDetallePage {
  nino?: Nino;

  constructor(
    private route: ActivatedRoute,
    private ninosService: NinosService
  ) {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.ninosService.getNino(id).subscribe(n => (this.nino = n));
  }
}
