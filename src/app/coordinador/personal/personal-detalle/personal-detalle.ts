import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';

import { Personal } from '../../../interfaces/personal.interface';
import { PersonalService } from '../../../service/personal.service';

@Component({
  selector: 'app-personal-detalle',
  standalone: true,
  templateUrl: './personal-detalle.html',
  styleUrls: ['./personal-detalle.scss'],
  imports: [CommonModule, MatIconModule]
})
export class PersonalDetalleComponent implements OnInit {

  personal?: Personal;
  cargando = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private personalService: PersonalService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.personalService.getPersonalById(id).subscribe({
      next: (p) => {
        this.personal = p;
        this.cargando = false;
      },
      error: () => {
        this.cargando = false;
      }
    });
  }

  volver(): void {
    this.router.navigate(['/coordinador/personal']);
  }

  editar(): void {
    if (!this.personal) return;
    this.router.navigate(['/coordinador/personal/editar', this.personal.id_personal]);
  }

  verHorarios(): void {
    if (!this.personal) return;
    this.router.navigate(['/coordinador/personal/horarios', this.personal.id_personal]);
  }
}
