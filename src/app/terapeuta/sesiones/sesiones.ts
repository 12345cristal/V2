import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { SesionesService, CrearSesionPayload } from '../../service/terapeuta/sesiones.service';
import { Sesion } from '../../interfaces/terapeuta/sesion.interface';

@Component({
  standalone: true,
  selector: 'app-sesiones-nino',
  imports: [CommonModule, FormsModule],
  templateUrl: './sesiones.html',
  styleUrls: ['./sesiones.scss'],
})
export class SesionesNinoPage {
  ninoId!: number;
  terapiaNinoId!: number;

  sesiones: Sesion[] = [];
  cargando = true;

  // Form nueva sesión
  fecha = this.nowLocalInputValue();
  asistio = true;
  progreso?: number;
  colaboracion?: number;
  observaciones = '';

  // UI edición
  editando: Record<number, boolean> = {};
  tmp: Record<number, Partial<Sesion>> = {};

  constructor(
    private route: ActivatedRoute,
    private sesionesService: SesionesService
  ) {
    this.ninoId = Number(this.route.snapshot.paramMap.get('ninoId'));

    const tn = this.route.snapshot.queryParamMap.get('terapiaNinoId');
    this.terapiaNinoId = tn ? Number(tn) : 0;

    this.cargar();
  }

  cargar() {
    this.cargando = true;

    const obs = this.terapiaNinoId
      ? this.sesionesService.getSesionesPorTerapiaNino(this.terapiaNinoId)
      : this.sesionesService.getSesionesPorNino(this.ninoId);

    obs.subscribe({
      next: data => {
        this.sesiones = data;
        this.sesiones.forEach(s => (this.tmp[s.id] = { ...s }));
      },
      complete: () => (this.cargando = false),
    });
  }

  crearSesion() {
    if (!this.terapiaNinoId) {
      alert('Falta terapiaNinoId');
      return;
    }

    const payload: CrearSesionPayload = {
      terapia_nino_id: this.terapiaNinoId,
      fecha: new Date(this.fecha).toISOString(),
      asistio: this.asistio,
      progreso: this.progreso ?? undefined,
      colaboracion: this.colaboracion ?? undefined,
      observaciones: this.observaciones.trim() || undefined,
    };

    this.sesionesService.crearSesion(payload).subscribe(() => {
      this.resetForm();
      this.cargar();
    });
  }

  empezarEditar(s: Sesion) {
    this.editando[s.id] = true;
    this.tmp[s.id] = { ...s };
  }

  cancelarEditar(id: number) {
    this.editando[id] = false;
    this.tmp[id] = {};
  }

  guardarEditar(s: Sesion) {
    const t = this.tmp[s.id];

    const payload: Partial<Omit<Sesion, 'id'>> = {
      asistio: t.asistio,
      progreso: t.progreso ?? undefined,
      colaboracion: t.colaboracion ?? undefined,
      observaciones: t.observaciones?.trim() || undefined,
    };

    this.sesionesService.actualizarSesion(s.id, payload).subscribe({
      next: () => {
        this.editando[s.id] = false;
        this.cargar();
      },
      error: () => {
        alert('Error al actualizar sesión');
        this.editando[s.id] = false;
      },
    });
  }

  resetForm() {
    this.fecha = this.nowLocalInputValue();
    this.asistio = true;
    this.progreso = undefined;
    this.colaboracion = undefined;
    this.observaciones = '';
  }

  formatFecha(fecha: string) {
    return new Date(fecha).toLocaleString();
  }

  private nowLocalInputValue(): string {
    const d = new Date();
    const pad = (n: number) => String(n).padStart(2, '0');
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(
      d.getHours()
    )}:${pad(d.getMinutes())}`;
  }
}
