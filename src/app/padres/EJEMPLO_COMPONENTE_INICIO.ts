// ============================================================================
// EJEMPLO DE USO DE INTERFACES - COMPONENTE INICIO
// ============================================================================

import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import {
  InicioPage,
  ProxSesion,
  UltimoAvance,
  TarjetaResumen,
  Hijo
} from '../padres.interfaces';
import { PadresService } from '../padres.service';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inicio.component.html',
  styleUrls: ['./inicio.component.css']
})
export class InicioComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  // Estado del componente
  inicioData: InicioPage | null = null;
  cargando = true;
  error: string | null = null;

  // Variables auxiliares
  saludo = '';
  horaActual: Date = new Date();
  hijoActual: Hijo | null = null;

  constructor(private padresService: PadresService) {
    this.actualizarSaludo();
    this.actualizarReloj();
  }

  ngOnInit(): void {
    this.cargarDatos();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  // ========================================================================
  // CARGA DE DATOS
  // ========================================================================

  private cargarDatos(): void {
    this.cargando = true;
    this.error = null;

    this.padresService
      .getInicioData()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (respuesta) => {
          if (respuesta.exito && respuesta.datos) {
            this.inicioData = respuesta.datos;
            this.hijoActual = respuesta.datos.hijoSeleccionado;
            this.cargando = false;
          } else {
            this.error = respuesta.error || 'Error al cargar los datos';
            this.cargando = false;
          }
        },
        error: (err) => {
          console.error('Error al cargar inicio:', err);
          this.error = 'Error de conexión. Por favor, intenta nuevamente.';
          this.cargando = false;
        }
      });
  }

  // ========================================================================
  // FUNCIONES DE UTILIDAD
  // ========================================================================

  private actualizarSaludo(): void {
    const hora = new Date().getHours();

    if (hora < 12) {
      this.saludo = 'Buenos días';
    } else if (hora < 18) {
      this.saludo = 'Buenas tardes';
    } else {
      this.saludo = 'Buenas noches';
    }
  }

  private actualizarReloj(): void {
    setInterval(() => {
      this.horaActual = new Date();
    }, 60000); // Actualizar cada minuto
  }

  // ========================================================================
  // INTERACCIONES CON TARJETAS
  // ========================================================================

  irAProxSesion(): void {
    if (this.inicioData?.tarjetas.proxSesion) {
      // Navegar a la sección de sesiones
      // this.router.navigate(['/padres/sesiones']);
    }
  }

  irAUltimoAvance(): void {
    if (this.inicioData?.tarjetas.ultimoAvance) {
      // Navegar a historial terapéutico
      // this.router.navigate(['/padres/historial-terapeutico']);
    }
  }

  irAPagos(): void {
    // this.router.navigate(['/padres/pagos']);
  }

  irADocumentos(): void {
    // this.router.navigate(['/padres/documentos']);
  }

  // ========================================================================
  // GESTIÓN DE HIJOS
  // ========================================================================

  cambiarHijo(hijo: Hijo): void {
    this.hijoActual = hijo;
    // Aquí podrías recargar datos del hijo específico si es necesario
    this.cargarDatos();
  }

  // ========================================================================
  // GETTERS PARA TEMPLATES
  // ========================================================================

  get proxSesion(): ProxSesion | null {
    return this.inicioData?.tarjetas.proxSesion ?? null;
  }

  get ultimoAvance(): UltimoAvance | null {
    return this.inicioData?.tarjetas.ultimoAvance ?? null;
  }

  get pagosPendientes(): number {
    return this.inicioData?.tarjetas.pagosPendientes.length ?? 0;
  }

  get documentosNuevos(): number {
    return this.inicioData?.tarjetas.documentosNuevos.filter(d => !d.visto).length ?? 0;
  }

  get tieneObservacion(): boolean {
    return !!this.inicioData?.tarjetas.ultimaObservacion;
  }

  // ========================================================================
  // FORMATEO DE DATOS
  // ========================================================================

  formatoFecha(fecha: Date): string {
    const date = new Date(fecha);
    return date.toLocaleDateString('es-ES', {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  }

  formatoHora(hora: string): string {
    // hora viene como "14:30" o similar
    return hora;
  }

  formatoMoneda(monto: number): string {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP'
    }).format(monto);
  }
}
