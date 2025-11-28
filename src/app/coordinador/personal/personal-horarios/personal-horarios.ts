import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';

import { Personal } from '../../../interfaces/personal.interface';
import { PersonalService } from '../../../service/personal.service';

@Component({
  selector: 'app-personal-horarios',
  standalone: true,
  templateUrl: './personal-horarios.html',
  styleUrls: ['./personal-horarios.scss'],
  imports: [CommonModule, MatIconModule]
})
export class PersonalHorariosComponent implements OnInit {

  personal?: Personal;
  cargando = true;

  dias = ['', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private personalService: PersonalService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.personalService.getPersonalById(id).subscribe({
      next: p => {
        this.personal = p;
        this.cargando = false;
      },
      error: () => this.cargando = false
    });
  }

  volver(): void {
    this.router.navigate(['/coordinador/personal']);
  }

  editarHorario(): void {
    if (!this.personal) return;
    // En caso de que quieras editar horarios después
  }

}
