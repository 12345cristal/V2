import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environment/environment';
import { DocumentoPadre } from '../interfaces/documento.interface';

@Injectable({ providedIn: 'root' })
export class DocumentosService {
  private baseUrl = `${environment.apiBaseUrl}/api/v1/documentos`;

  constructor(private http: HttpClient) {}

  listar(usuarioId: number, tipo?: string) {
    let url = `${this.baseUrl}?usuario_id=${usuarioId}`;
    if (tipo) url += `&tipo=${tipo}`;
    return this.http.get<DocumentoPadre[]>(url);
  }

  obtener(documentoId: number) {
    return this.http.get<DocumentoPadre>(`${this.baseUrl}/${documentoId}`);
  }

  subir(file: File, usuarioId: number, titulo?: string) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('usuario_id', usuarioId.toString());
    if (titulo) formData.append('titulo', titulo);
    return this.http.post<DocumentoPadre>(this.baseUrl, formData);
  }

  eliminar(documentoId: number, usuarioId: number) {
    return this.http.delete<any>(`${this.baseUrl}/${documentoId}?usuario_id=${usuarioId}`);
  }

  actualizar(documentoId: number, titulo: string, usuarioId: number) {
    return this.http.put<any>(`${this.baseUrl}/${documentoId}?titulo=${titulo}&usuario_id=${usuarioId}`, {});
  }

  // Alias que tu componente espera
  getDocumentos(usuarioId: number, tipo?: string) {
    return this.listar(usuarioId, tipo);
  }

  // Marca como visto (ajusta si tu backend tiene un endpoint específico)
  marcarVisto(documentoId: number, usuarioId: number) {
    return this.http.put<any>(
      `${this.baseUrl}/${documentoId}?usuario_id=${usuarioId}`,
      { visto: true }
    );
  }

  // Descarga como Blob
  descargar(documentoId: number) {
    return this.http.get(`${this.baseUrl}/${documentoId}`, { responseType: 'blob' });
  }
}
