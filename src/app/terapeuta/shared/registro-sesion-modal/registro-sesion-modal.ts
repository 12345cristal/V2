import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { TerapeutaService, RegistroSesionDTO } from '../../../service/terapeuta.service';

@Component({
  selector: 'app-registro-sesion-modal',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatIconModule],
  templateUrl: './registro-sesion-modal.html',
  styleUrls: ['./registro-sesion-modal-mejorado.scss']
})
export class RegistroSesionModalComponent implements OnInit {
  @Input() ninoId!: number;
  @Input() ninoNombre!: string;
  @Output() cerrar = new EventEmitter<void>();
  @Output() sesionRegistrada = new EventEmitter<any>();

  formSesion!: FormGroup;
  archivosSeleccionados: File[] = [];
  guardando = false;

  constructor(
    private fb: FormBuilder,
    private terapeutaService: TerapeutaService
  ) {}

  ngOnInit(): void {
    this.initForm();
  }

  private initForm(): void {
    this.formSesion = this.fb.group({
      // Información clínica interna
      actividadesRealizadas: ['', [Validators.required]],
      respuestaNino: ['', [Validators.required]],
      observacionesClinicas: [''],
      incidentes: [''],

      // Información para padres
      resumenPadres: ['', [Validators.required]],
      queHacer: ['', [Validators.required]],
      queEvitar: [''],
      rutinasSugeridas: [''],
      materialesRecomendados: ['']
    });
  }

  onFileSelect(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      this.archivosSeleccionados = Array.from(input.files);
    }
  }

  guardarBorrador(): void {
    const borrador = {
      ...this.formSesion.value,
      id_nino: this.ninoId,
      estado: 'borrador',
      fecha: new Date().toISOString()
    };
    
    // Guardar en localStorage temporalmente
    localStorage.setItem(`borrador_sesion_${this.ninoId}`, JSON.stringify(borrador));
    alert('Borrador guardado correctamente');
  }

  guardarSesion(): void {
    if (this.formSesion.invalid) {
      alert('Por favor completa todos los campos obligatorios');
      Object.keys(this.formSesion.controls).forEach(key => {
        const control = this.formSesion.get(key);
        if (control?.invalid) {
          control.markAsTouched();
        }
      });
      return;
    }

    this.guardando = true;

    const sesionDTO: RegistroSesionDTO = {
      id_nino: this.ninoId,
      fecha: new Date().toISOString(),
      
      informacionClinica: {
        actividadesRealizadas: this.formSesion.value.actividadesRealizadas,
        respuestaNino: this.formSesion.value.respuestaNino,
        observacionesClinicas: this.formSesion.value.observacionesClinicas,
        incidentes: this.formSesion.value.incidentes,
        evidencias: this.archivosSeleccionados
      },
      
      informacionPadres: {
        resumenSesion: this.formSesion.value.resumenPadres,
        guiaParaCasa: {
          queHacer: this.formSesion.value.queHacer,
          queEvitar: this.formSesion.value.queEvitar,
          rutinasSugeridas: this.formSesion.value.rutinasSugeridas,
          materialesRecomendados: this.formSesion.value.materialesRecomendados
        }
      }
    };

    this.terapeutaService.registrarSesion(sesionDTO).subscribe({
      next: (response) => {
        console.log('Sesión registrada exitosamente:', response);
        alert('Sesión registrada exitosamente');
        
        // Limpiar borrador si existe
        localStorage.removeItem(`borrador_sesion_${this.ninoId}`);
        
        this.sesionRegistrada.emit(response);
        this.cerrarModal();
      },
      error: (error) => {
        console.error('Error al registrar sesión:', error);
        alert(`Error al registrar la sesión: ${error.message}`);
        this.guardando = false;
      },
      complete: () => {
        this.guardando = false;
      }
    });
  }

  cerrarModal(): void {
    if (this.formSesion.dirty && !confirm('¿Seguro que deseas salir? Los cambios no guardados se perderán.')) {
      return;
    }
    this.cerrar.emit();
  }
}
