import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MatIconModule } from '@angular/material/icon';

import { PersonalService } from '../../../service/personal.service';
import { Personal, Rol } from '../../../interfaces/personal.interface';
import { NotificationService } from '../../../shared/notification.service';

@Component({
  selector: 'app-personal-form',
  standalone: true,
  templateUrl: './personal-form.html',
  styleUrls: ['./personal-form.scss'],
  imports: [CommonModule, ReactiveFormsModule, MatIconModule]
})
export class PersonalFormComponent implements OnInit {

  formulario!: FormGroup;
  roles: Rol[] = [];
  idEditar?: number;

  fotoPreview: string | null = null;
  errorFoto = '';
  enviando = false;
  error = '';

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private personalService: PersonalService,
    private notificationService: NotificationService
  ) {}

  ngOnInit(): void {
    this.idEditar = Number(this.route.snapshot.paramMap.get('id')) || undefined;
    this.crearFormulario();
    this.cargarRoles();

    if (this.idEditar) this.cargarPersonal();
  }

  /* ========================================
     🔥 GETTERS — Sin errores NG4111
     ======================================== */
  get nombres() { return this.formulario.get('nombres')!; }
  get apellido_paterno() { return this.formulario.get('apellido_paterno')!; }
  get apellido_materno() { return this.formulario.get('apellido_materno')!; }
  get id_rol() { return this.formulario.get('id_rol')!; }
  get telefono_personal() { return this.formulario.get('telefono_personal')!; }
  get correo_personal() { return this.formulario.get('correo_personal')!; }
  get rfc() { return this.formulario.get('rfc')!; }
  get curp() { return this.formulario.get('curp')!; }
  get experiencia() { return this.formulario.get('experiencia')!; }

  private crearFormulario(): void {
    const soloLetras = /^[a-zA-ZÁÉÍÓÚÑáéíóúñ ]+$/;

    this.formulario = this.fb.group({
      nombres: ['', [Validators.required, Validators.minLength(3), Validators.pattern(soloLetras)]],
      apellido_paterno: ['', [Validators.required, Validators.pattern(soloLetras)]],
      apellido_materno: ['', Validators.pattern(soloLetras)],
      id_rol: [null, Validators.required],

      especialidad_principal: ['', Validators.required],

      telefono_personal: ['', [Validators.required, Validators.pattern(/^\d{10}$/)]],
      correo_personal: ['', [Validators.required, Validators.email]],

      fecha_ingreso: ['', Validators.required],
      fecha_nacimiento: ['', Validators.required],

      // 🔥 Validaciones EXACTAS del backend
      rfc: ['', [Validators.required, Validators.minLength(13), Validators.maxLength(13)]],
      curp: ['', [Validators.required, Validators.minLength(18), Validators.maxLength(18)]],

      domicilio_calle: ['', Validators.required],
      domicilio_colonia: ['', Validators.required],
      domicilio_cp: ['', Validators.required],
      domicilio_municipio: ['', Validators.required],
      domicilio_estado: ['', Validators.required],

      experiencia: ['', [Validators.required, Validators.minLength(20)]],

      foto: [null]
    });
  }

  private cargarRoles(): void {
    this.personalService.getRoles().subscribe({
      next: roles => this.roles = roles
    });
  }

  private cargarPersonal(): void {
    if (!this.idEditar) return;

    this.personalService.getPersonalById(this.idEditar).subscribe({
      next: (p: Personal) => this.formulario.patchValue(p)
    });
  }

  /* ========================================
     📸 Selección de FOTO (100% funcional)
     ======================================== */
  onSeleccionarFoto(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    this.errorFoto = '';

    if (!file) return;

    if (!['image/png', 'image/jpeg', 'image/jpg'].includes(file.type)) {
      this.errorFoto = 'La foto debe ser JPG o PNG';
      return;
    }

    if (file.size > 3 * 1024 * 1024) {
      this.errorFoto = 'La foto no puede pesar más de 3 MB';
      return;
    }

    this.formulario.patchValue({ foto: file });

    const reader = new FileReader();
    reader.onload = () => this.fotoPreview = reader.result as string;
    reader.readAsDataURL(file);
  }

  guardar(): void {
    if (this.formulario.invalid) {
      this.formulario.markAllAsTouched();
      this.error = 'Faltan campos obligatorios o contienen errores.';
      return;
    }

    this.enviando = true;
    this.error = '';

    const formData = new FormData();
    const raw = this.formulario.value;

    Object.keys(raw).forEach(key => {
      const valor = (raw as any)[key];
      if (valor !== null && valor !== undefined)
        formData.append(key, valor);
    });

    const obs = this.idEditar
      ? this.personalService.updatePersonal(this.idEditar, formData)
      : this.personalService.createPersonal(formData);

    obs.subscribe({
      next: () => {
        this.enviando = false;
        const mensaje = this.idEditar 
          ? 'Personal actualizado correctamente'
          : 'Personal creado correctamente';
        this.notificationService.success(mensaje);
        this.router.navigate(['/coordinador/personal']);
      },
      error: (err) => {
        this.enviando = false;
        this.error = 'Ocurrió un error al guardar el registro.';
        this.notificationService.error('No se pudo guardar el personal');
      }
    });
  }

  cancelar(): void {
    this.router.navigate(['/coordinador/personal']);
  }
}
