import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {
  CrearDocumentoPadreDto,
  DocumentoPadre,
  DocumentoTerapeuta,
} from '../interfaces/documento.interface';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({ providedIn: 'root' })
export class DocumentosService {

  private base = environment.apiBaseUrl + '/documentos';

  constructor(private http: HttpClient) {}

  getTerapeutaDocs(id: number): Observable<DocumentoTerapeuta[]> {
    return this.http.get<DocumentoTerapeuta[]>(`${this.base}/terapeuta/${id}`);
  }

  getPadreDocs(id: number): Observable<DocumentoPadre[]> {
    return this.http.get<DocumentoPadre[]>(`${this.base}/padre/${id}`);
  }

  subirDocumento(dto: CrearDocumentoPadreDto): Observable<DocumentoPadre> {
    const fd = new FormData();
    Object.keys(dto).forEach(key => fd.append(key, (dto as any)[key]));
    return this.http.post<DocumentoPadre>(`${this.base}/padre`, fd);
  }

  eliminar(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}/padre/${id}`);
  }
}
