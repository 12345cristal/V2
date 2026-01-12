import { Injectable, signal } from '@angular/core';
import { Hijo } from '../interfaces/hijo.interface';

@Injectable({ providedIn: 'root' })
export class PadreHijosStateService {
  hijos = signal<Hijo[]>([]);
  seleccionadoId = signal<number | null>(null);

  setHijos(lista: Hijo[]) {
    this.hijos.set(lista);
    if (lista.length && !this.seleccionadoId()) this.seleccionadoId.set(lista[0].id);
  }

  addHijo(h: Hijo) {
    const lista = [h, ...this.hijos()];
    this.hijos.set(lista);
    if (!this.seleccionadoId()) this.seleccionadoId.set(h.id);
  }

  updateHijo(h: Hijo) {
    this.hijos.set(this.hijos().map(x => (x.id === h.id ? h : x)));
  }

  removeHijo(id: number) {
    const lista = this.hijos().filter(x => x.id !== id);
    this.hijos.set(lista);
    if (this.seleccionadoId() === id) this.seleccionadoId.set(lista[0]?.id ?? null);
  }

  seleccionar(id: number) {
    this.seleccionadoId.set(id);
  }
}
