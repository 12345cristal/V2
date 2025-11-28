import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  // rol actual: coordinador | terapeuta | padre
private rol: string = 'terapeuta';

  setRol(newRol: string) {
    this.rol = newRol;
  }

  getRol(): string {
    return this.rol;
  }
}
