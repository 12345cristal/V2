import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  // Simulación local mientras tú manejas roles
  private rol: string = 'coordinador';

  // URL del login del backend FastAPI
  private apiUrl = 'http://localhost:8000/auth/login'; // AJÚSTALO A TU API

  constructor(private http: HttpClient) {}

  // ============================
  // 🟦 MÉTODO REAL DE LOGIN
  // ============================
  login(correo: string, contrasena: string): Observable<any> {
    return this.http.post(this.apiUrl, {
      correo,
      contrasena,
    });
  }

  // ============================
  // 🟨 CONTROL INTERNO DE ROL
  // ============================
  setRol(newRol: string) {
    this.rol = newRol;
  }

  getRol(): string {
    return this.rol;
  }
}
