import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormArray,
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { NinosService } from '../../../service/ninos.service';
import { Nino } from '../../../interfaces/nino.interface';

@Component({
  selector: 'app-nino-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './nino-form.html',
styleUrls: ['./nino-form.scss']
})
export class NinoForm implements OnInit {

  formulario!: FormGroup;
  step = 1;
  isEdit = false;
  idNino?: number;

  // Archivos
  actaNacimientoFile?: File | null;
  curpFile?: File | null;
  comprobanteFile?: File | null;
  fotoFile?: File | null;
  diagnosticoFile?: File | null;
  consentimientoFile?: File | null;
  hojaIngresoFile?: File | null;

  submitError = '';
  submitting = false;

  constructor(
    private fb: FormBuilder,
    private ninosService: NinosService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.buildForm();

    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (id) {
        this.isEdit = true;
        this.idNino = +id;
        this.cargarNino(+id);
      }
    });

    // Autocalcular edad
    this.formulario.get('fechaNacimiento')?.valueChanges.subscribe(value => {
      if (value) {
        const edad = this.calcularEdad(value);
        this.formulario.get('edad')?.setValue(edad, { emitEvent: false });
      } else {
        this.formulario.get('edad')?.setValue(null, { emitEvent: false });
      }
    });
  }

  /* ============================================
     🧱 BUILD FORM COMPLETO
  ============================================ */
  private buildForm(): void {
    this.formulario = this.fb.group({
      // 1. Datos personales
      nombre: ['', [Validators.required, Validators.minLength(2)]],
      apellidoPaterno: ['', Validators.required],
      apellidoMaterno: ['', Validators.required],
      fechaNacimiento: ['', Validators.required],
      edad: [{ value: null, disabled: true }],
      sexo: ['M', Validators.required],
      curp: [''],

      direccion: this.fb.group({
        calle: [''],
        numero: [''],
        colonia: [''],
        municipio: [''],
        codigoPostal: ['']
      }),

      // 2. Info médica
      diagnostico: this.fb.group({
        diagnosticoPrincipal: ['', Validators.required],
        fechaDiagnostico: [''],
        diagnosticosSecundarios: [[]],
        especialista: [''],
        institucion: ['']
      }),

      alergias: this.fb.group({
        medicamentos: [''],
        alimentos: [''],
        ambiental: ['']
      }),

      medicamentosActuales: this.fb.array([]),

      // 3. Escolar
      escolar: this.fb.group({
        escuela: [''],
        grado: [''],
        maestro: [''],
        horarioClases: [''],
        adaptaciones: ['']
      }),

      // 4. Padres / tutores
      padre: this.fb.group({
        nombreCompleto: ['', Validators.required],
        fechaNacimiento: [''],
        telefono: ['', Validators.required],
        telefonoSecundario: [''],
        correo: ['', Validators.email],
        ocupacion: [''],
        direccionLaboral: ['']
      }),

      madre: this.fb.group({
        nombreCompleto: [''],
        telefono: [''],
        telefonoSecundario: [''],
        correo: ['', Validators.email]
      }),

      tutorLegal: this.fb.group({
        nombreCompleto: [''],
        relacion: [''],
        telefono: [''],
        telefonoSecundario: [''],
        correo: ['', Validators.email],
        esTutorLegal: [false]
      }),

      contactosEmergencia: this.fb.array([
        this.buildContactoEmergencia(),
        this.buildContactoEmergencia()
      ]),

      // 5. Info emocional
      infoEmocional: this.fb.group({
        estimulos: [''],
        calmantes: [''],
        preferencias: [''],
        noTolera: [''],
        palabrasClave: [''],
        formaComunicacion: [''],
        nivelComprension: ['MEDIO']
      }),

      // 6. Info centro
      infoCentro: this.fb.group({
        fechaIngreso: ['', Validators.required],
        costoMensual: [0],
        modalidadPago: [''],
        terapeutaAsignado: [''],
        horariosTerapia: [''],
        estado: ['ACTIVO', Validators.required],

        terapias: this.fb.group({
          lenguaje: [false],
          conductual: [false],
          ocupacional: [false],
          sensorial: [false],
          psicologia: [false]
        })
      })
    });
  }

  private buildContactoEmergencia(): FormGroup {
    return this.fb.group({
      nombreCompleto: ['', Validators.required],
      relacion: ['', Validators.required],
      telefono: ['', Validators.required],
      telefonoSecundario: ['']
    });
  }

  /* ============================================
     🧠 GETTERS
  ============================================ */
  get medicamentosArray(): FormArray {
    return this.formulario.get('medicamentosActuales') as FormArray;
  }

  get contactosArray(): FormArray {
    return this.formulario.get('contactosEmergencia') as FormArray;
  }

  get diagnosticosSecundariosString(): string {
    return this.formulario.get('diagnostico.diagnosticosSecundarios')?.value?.join(', ') ?? '';
  }

  updateDiagnosticosSecundarios(event: Event): void {
    const value = (event.target as HTMLInputElement).value;
    const lista = value.split(',').map(v => v.trim()).filter(v => v !== '');
    this.formulario.get('diagnostico.diagnosticosSecundarios')?.setValue(lista);
  }

  /* ============================================
     🧩 MÉTODOS FORMARRAY
  ============================================ */
  agregarMedicamento(): void {
    this.medicamentosArray.push(
      this.fb.group({
        nombre: ['', Validators.required],
        dosis: [''],
        horario: ['']
      })
    );
  }

  eliminarMedicamento(index: number): void {
    this.medicamentosArray.removeAt(index);
  }

  agregarContacto(): void {
    this.contactosArray.push(this.buildContactoEmergencia());
  }

  eliminarContacto(index: number): void {
    if (this.contactosArray.length > 2) {
      this.contactosArray.removeAt(index);
    }
  }

  /* ============================================
     📥 CARGAR NIÑO
  ============================================ */
  private cargarNino(id: number): void {
    this.ninosService.getNino(id).subscribe(n => {
      this.formulario.patchValue(n);

      // medicamentos
      this.medicamentosArray.clear();
      n.medicamentosActuales?.forEach(m =>
        this.medicamentosArray.push(
          this.fb.group({
            nombre: [m.nombre, Validators.required],
            dosis: [m.dosis],
            horario: [m.horario]
          })
        )
      );

      // contactos
      this.contactosArray.clear();
      n.contactosEmergencia?.forEach(c =>
        this.contactosArray.push(
          this.fb.group({
            nombreCompleto: [c.nombreCompleto, Validators.required],
            relacion: [c.relacion, Validators.required],
            telefono: [c.telefono, Validators.required],
            telefonoSecundario: [c.telefonoSecundario]
          })
        )
      );
    });
  }

  /* ============================================
     🔄 NAVEGACIÓN DE PASOS
  ============================================ */
  goToStep(target: number): void {
    if (target < 1 || target > 5) return;
    this.step = target;
    this.submitError = '';
  }

  nextStep(): void {
    if (!this.isCurrentStepValid()) {
      this.submitError = 'Completa los campos obligatorios del paso actual.';
      return;
    }
    if (this.step < 5) {
      this.step++;
      this.submitError = '';
    }
  }

  prevStep(): void {
    if (this.step > 1) {
      this.step--;
      this.submitError = '';
    }
  }

  private isCurrentStepValid(): boolean {
    const requiredGroups: Record<number, string[]> = {
      1: ['nombre', 'apellidoPaterno', 'apellidoMaterno', 'fechaNacimiento', 'sexo'],
      2: ['diagnostico'],
      3: ['escolar'],
      4: ['padre', 'contactosEmergencia'],
      5: ['infoCentro']
    };

    const controls = requiredGroups[this.step] ?? [];

    controls.forEach(name => this.formulario.get(name)?.markAllAsTouched());

    return controls.every(name => this.formulario.get(name)?.valid);
  }

  /* ============================================
     📂 ARCHIVOS
  ============================================ */
  onFileChange(event: Event, type: string): void {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const file = input.files[0];

    switch (type) {
      case 'acta': this.actaNacimientoFile = file; break;
      case 'curp': this.curpFile = file; break;
      case 'comprobante': this.comprobanteFile = file; break;
      case 'foto': this.fotoFile = file; break;
      case 'diagnostico': this.diagnosticoFile = file; break;
      case 'consentimiento': this.consentimientoFile = file; break;
      case 'hojaIngreso': this.hojaIngresoFile = file; break;
    }
  }

  /* ============================================
     💾 GUARDAR
  ============================================ */
  guardar(): void {
    this.submitError = '';
    this.formulario.markAllAsTouched();

    if (this.formulario.invalid) {
      this.submitError = 'Revisa los campos marcados en rojo.';
      return;
    }

    this.submitting = true;

    const nino: Nino = {
      ...this.formulario.getRawValue(),
      edad: this.formulario.get('edad')?.value
    };

    const archivos = {
      actaNacimiento: this.actaNacimientoFile,
      curp: this.curpFile,
      comprobanteDomicilio: this.comprobanteFile,
      foto: this.fotoFile,
      diagnostico: this.diagnosticoFile,
      consentimiento: this.consentimientoFile,
      hojaIngreso: this.hojaIngresoFile
    };

    const obs = this.isEdit && this.idNino
      ? this.ninosService.updateNino(this.idNino, { nino, archivos })
      : this.ninosService.createNino({ nino, archivos });

    obs.subscribe({
      next: () => {
        this.submitting = false;
        this.router.navigate(['/coordinador/ninos']);
      },
      error: () => {
        this.submitting = false;
        this.submitError = 'Ocurrió un error al guardar. Intenta de nuevo.';
      }
    });
  }

  cancelar(): void {
    this.router.navigate(['/coordinador/ninos']);
  }

  private calcularEdad(fecha: string): number {
    const nacimiento = new Date(fecha);
    const hoy = new Date();
    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    const m = hoy.getMonth() - nacimiento.getMonth();

    if (m < 0 || (m === 0 && hoy.getDate() < nacimiento.getDate())) {
      edad--;
    }

    return edad;
  }
  isInvalid(path: string): boolean {
  const control = this.formulario.get(path);
  return !!control && control.invalid && (control.touched || control.dirty);
}

}
