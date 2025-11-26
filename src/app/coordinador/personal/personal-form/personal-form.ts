import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { PersonalService } from '../../../service/personal.service';

@Component({
  selector: 'app-personal-form',
  standalone: true,
  templateUrl: './personal-form.html',
  styleUrls: ['./personal-form.scss'],
})
export class PersonalFormComponent implements OnInit {

  id!: number;
  editMode = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private service: PersonalService
  ) {}

  ngOnInit(): void {
    document.getElementById('btnVolver')!
      .addEventListener('click', () => this.router.navigate(['/coordinador/personal']));

    // Detectar modo edición
    this.id = Number(this.route.snapshot.paramMap.get('id'));
    this.editMode = !!this.id;

    if (this.editMode) this.cargar();

    document.getElementById('btnGuardar')!
      .addEventListener('click', () => this.guardar());
  }

  cargar() {
    this.service.getPersonalById(this.id).subscribe(p => {
      (document.getElementById('inputNombre') as HTMLInputElement).value = p.nombre_completo;
      (document.getElementById('inputEspec') as HTMLInputElement).value = p.especialidad_principal ?? '';
      (document.getElementById('inputCorreo') as HTMLInputElement).value = p.correo_personal ?? '';
      (document.getElementById('inputTel') as HTMLInputElement).value = p.telefono_personal ?? '';
    });
  }

  guardar() {
    const dto = {
      id_usuario: null, // 🔥 clave para no generar errores
      nombre_completo: (document.getElementById('inputNombre') as HTMLInputElement).value,
      especialidad_principal: (document.getElementById('inputEspec') as HTMLInputElement).value,
      correo_personal: (document.getElementById('inputCorreo') as HTMLInputElement).value,
      telefono_personal: (document.getElementById('inputTel') as HTMLInputElement).value,
      activo: true
    };

    if (this.editMode) {
      this.service.updatePersonal(this.id, dto).subscribe(() => {
        this.router.navigate(['/coordinador/personal']);
      });
    } else {
      this.service.createPersonal(dto).subscribe(() => {
        this.router.navigate(['/coordinador/personal']);
      });
    }
  }
}
