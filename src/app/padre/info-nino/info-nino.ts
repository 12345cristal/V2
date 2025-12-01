// src/app/padre/info-nino/info-nino.ts

import {
  Component,
  OnInit,
  signal,
  computed
} from '@angular/core';
import { CommonModule } from '@angular/common';
  import { ActivatedRoute, RouterModule } from '@angular/router';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';

import { Nino } from '../../interfaces/nino.interface';
import { NinosService } from '../../service/nino.service';

@Component({
  selector: 'app-info-nino',
  standalone: true,
  imports: [CommonModule, RouterModule, ReactiveFormsModule],
  templateUrl: './info-nino.html',
  styleUrls: ['./info-nino.scss']
})
export class InfoNinoComponent implements OnInit {

  nino = signal<Nino | null>(null);
  cargando = signal<boolean>(false);
  guardando = signal<boolean>(false);
  error = signal<string | null>(null);
  mensajeExito = signal<string | null>(null);

  puedeEditar = signal<boolean>(true);
  modoEdicion = signal<boolean>(false);

  datosForm!: FormGroup;
  diagnosticoForm!: FormGroup;

  edadCalculada = computed(() => {
    const niño = this.nino();
    if (!niño) return null;
    return this.calcularEdad(niño.fechaNacimiento);
  });

  constructor(
    private route: ActivatedRoute,
    private ninosService: NinosService,
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    this.inicializarFormularios();
    this.cargarNino();
  }

  private inicializarFormularios(): void {
    this.datosForm = this.fb.group({
      nombre: ['', Validators.required],
      apellidoPaterno: ['', Validators.required],
      apellidoMaterno: ['', Validators.required],
      fechaNacimiento: ['', Validators.required],
      sexo: ['', Validators.required],
      curp: ['']
    });

    this.diagnosticoForm = this.fb.group({
      diagnosticoPrincipal: ['', Validators.required],
      fechaDiagnostico: [''],
      diagnosticosSecundariosTexto: [''],
      especialista: [''],
      institucion: ['']
    });

    this.datosForm.disable();
    this.diagnosticoForm.disable();
  }

  private cargarNino(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!id) {
      this.error.set('ID inválido');
      return;
    }

    this.cargando.set(true);

    this.ninosService.obtenerNinoPorId(id).subscribe({
      next: (nino: Nino) => {
        this.nino.set(nino);
        this.patchForms(nino);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set('No se pudo cargar la información.');
        this.cargando.set(false);
      }
    });
  }

  private patchForms(nino: Nino): void {
    this.datosForm.patchValue({
      nombre: nino.nombre,
      apellidoPaterno: nino.apellidoPaterno,
      apellidoMaterno: nino.apellidoMaterno,
      fechaNacimiento: nino.fechaNacimiento,
      sexo: nino.sexo,
      curp: nino.curp ?? ''
    });

    const dx = nino.diagnostico;

    this.diagnosticoForm.patchValue({
      diagnosticoPrincipal: dx.diagnosticoPrincipal,
      fechaDiagnostico: dx.fechaDiagnostico,
      diagnosticosSecundariosTexto: (dx.diagnosticosSecundarios || []).join(', '),
      especialista: dx.especialista,
      institucion: dx.institucion
    });
  }

  activarEdicion(): void {
    if (!this.puedeEditar()) return;
    this.modoEdicion.set(true);
    this.datosForm.enable();
    this.diagnosticoForm.enable();
    this.datosForm.get('curp')?.disable();
  }

  cancelarEdicion(): void {
    const niño = this.nino();
    if (!niño) return;
    this.modoEdicion.set(false);
    this.datosForm.disable();
    this.diagnosticoForm.disable();
    this.patchForms(niño);
  }

  guardarCambios(): void {
    const niño = this.nino();
    if (!niño) return;

    const datos = this.datosForm.getRawValue();
    const dx = this.diagnosticoForm.value;

    const diagnosticosSecundarios = (dx.diagnosticosSecundariosTexto || '')
      .split(',')
      .map((x: string) => x.trim())
      .filter((x: string) => x);

    const payload: Partial<Nino> = {
      nombre: datos.nombre,
      apellidoPaterno: datos.apellidoPaterno,
      apellidoMaterno: datos.apellidoMaterno,
      fechaNacimiento: datos.fechaNacimiento,
      sexo: datos.sexo,

      diagnostico: {
        ...niño.diagnostico,
        diagnosticoPrincipal: dx.diagnosticoPrincipal,
        fechaDiagnostico: dx.fechaDiagnostico || null,
        diagnosticosSecundarios,
        especialista: dx.especialista,
        institucion: dx.institucion
      }
    };

    this.guardando.set(true);

    this.ninosService.actualizarNino(niño.id!, payload).subscribe({
      next: (actualizado: Nino) => {
        this.nino.set(actualizado);
        this.patchForms(actualizado);
        this.modoEdicion.set(false);
        this.guardando.set(false);
        this.mensajeExito.set('Cambios guardados correctamente.');
      },
      error: () => {
        this.guardando.set(false);
        this.error.set('Error al guardar.');
      }
    });
  }

  private calcularEdad(fechaNacimiento: string): number | null {
    if (!fechaNacimiento) return null;

    const f = new Date(fechaNacimiento);
    const hoy = new Date();

    let edad = hoy.getFullYear() - f.getFullYear();
    const m = hoy.getMonth() - f.getMonth();
    if (m < 0 || (m === 0 && hoy.getDate() < f.getDate())) edad--;

    return edad;
  }

  obtenerNombreCompleto(): string {
    const n = this.nino();
    if (!n) return '';
    return `${n.nombre} ${n.apellidoPaterno} ${n.apellidoMaterno}`.trim();
  }
}
