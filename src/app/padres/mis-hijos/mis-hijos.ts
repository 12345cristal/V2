import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PadresService } from '../padres.service';
import { Hijo, MisHijosPage } from '../padres.interfaces';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

@Component({
  selector: 'app-mis-hijos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './mis-hijos.html',
  styleUrl: './mis-hijos.scss',
})
export class MisHijos implements OnInit, OnDestroy {
  hijos: Hijo[] = [];
  hijoSeleccionado: Hijo | null = null;
  cargando = true;
  private destroy$ = new Subject<void>();

  constructor(private padresService: PadresService) {}

  ngOnInit(): void {
    this.cargarHijos();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  cargarHijos(): void {
    this.cargando = true;
    this.padresService
      .getMisHijos()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (respuesta) => {
          if (respuesta.exito && respuesta.datos) {
            this.hijos = respuesta.datos.hijos;
            if (this.hijos.length > 0) {
              this.seleccionarHijo(this.hijos[0]);
            }
          }
          this.cargando = false;
        },
        error: (err) => {
          console.error('Error al cargar hijos:', err);
          this.cargando = false;
        }
      });
  }

  seleccionarHijo(hijo: Hijo): void {
    this.hijoSeleccionado = hijo;
    if (hijo.novedades > 0) {
      this.marcarVisto(hijo.id);
    }
  }

  marcarVisto(hijoId: number): void {
    // Implementar cuando haya endpoint
    const hijo = this.hijos.find(h => h.id === hijoId);
    if (hijo) {
      hijo.visto = true;
      hijo.novedades = 0;
    }
  }

  calcularEdad(fechaNacimiento: string): number {
    const hoy = new Date();
    const nacimiento = new Date(fechaNacimiento);
    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    const mes = hoy.getMonth() - nacimiento.getMonth();
    
    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
      edad--;
    }
    
    return edad;
  }

  obtenerSeveridadColor(severidad: string): string {
    const colores: { [key: string]: string } = {
      'leve': 'severidad-leve',
      'moderada': 'severidad-moderada',
      'severa': 'severidad-severa'
    };
    return colores[severidad] || 'severidad-leve';
  }

  obtenerMedicamentoNuevo(medicamento: any): boolean {
    return medicamento.novedadReciente === true;
  }
}
