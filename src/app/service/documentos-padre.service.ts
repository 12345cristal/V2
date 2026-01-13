import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { DocumentoPadre, RespuestaDocumentos } from '../interfaces/documento.interface';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DocumentosPadreService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/api/v1/documentos`;

  getDocumentos(hijoId: number): Observable<DocumentoPadre[]> {
    return this.http.get<RespuestaDocumentos>(
      `${this.apiUrl}/hijo/${hijoId}`
    ).pipe(
      map((respuesta: RespuestaDocumentos) => {
        if (respuesta.success && respuesta.data) {
          return respuesta.data.map((doc: DocumentoPadre) => ({
            ...doc,
            key: doc.id
          }));
        }
        return [];
      }),
      catchError((error: unknown) => {
        console.error('Error al cargar documentos:', error);
        return of([]);
      })
    );
  }

  marcarVisto(documentoId: number): Observable<any> {
    return this.http.post(
      `${this.apiUrl}/${documentoId}/visto`,
      {}
    );
  }

  descargar(url: string, nombreArchivo?: string): void {
    window.open(url, '_blank');
  }

  subirDocumento(
    hijoId: number,
    archivo: File,
    tipo: string,
    nombre: string,
    descripcion?: string
  ): Observable<DocumentoPadre> {
    const formData = new FormData();
    formData.append('archivo', archivo);
    formData.append('tipo', tipo);
    formData.append('nombre', nombre);
    if (descripcion) {
      formData.append('descripcion', descripcion);
    }

    return this.http.post<DocumentoPadre>(
      `${this.apiUrl}/hijo/${hijoId}/upload`,
      formData
    );
  }

  eliminarDocumento(documentoId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${documentoId}`);
  }
}

