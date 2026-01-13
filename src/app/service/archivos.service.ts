import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Injectable({ providedIn: 'root' })
export class ArchivosService {
  private http = inject(HttpClient);
  private sanitizer = inject(DomSanitizer);

  /**
   * Descarga un archivo protegido como Blob
   */
  descargarComoBlob(ruta: string, token?: string): Observable<Blob> {
    // Si es una ruta relativa, convertir a URL absoluta
    let url = ruta;
    if (!ruta.startsWith('http://') && !ruta.startsWith('https://')) {
      // Es una ruta relativa: "cv/personal_1_..." -> "/api/v1/perfil/archivos/cv/personal_1_..."
      const partes = ruta.split('/');
      if (partes.length >= 2) {
        const tipo = partes[0];
        const filename = partes.slice(1).join('/');
        url = `/api/v1/perfil/archivos/${tipo}/${filename}`;
      }
    }

    const headers = token
      ? new HttpHeaders({ Authorization: `Bearer ${token}` })
      : undefined;

    return this.http.get(url, {
      responseType: 'blob',
      headers,
    });
  }

  /**
   * Crea una URL segura para visualizar un PDF en un iframe
   * Usa el endpoint /visualizar para PDFs
   */
  obtenerUrlPdfParaVisualizar(ruta: string): SafeResourceUrl {
    // Manejar tanto rutas relativas como URLs completas
    let cleanRuta = ruta;
    
    // Si es una URL completa, extraer solo la ruta relativa
    if (ruta.startsWith('http://') || ruta.startsWith('https://')) {
      const url = new URL(ruta);
      // Extraer de /api/v1/perfil/archivos/cv/filename -> cv/filename
      const pathname = url.pathname;
      const match = pathname.match(/\/api\/v1\/perfil\/archivos\/(.+)/);
      if (match) {
        cleanRuta = match[1];
      }
    }
    
    // Convertir ruta relativa a URL de visualización
    // Ejemplo: "cv/personal_1_1700000000_cv.pdf" -> "/api/v1/perfil/archivos/cv/personal_1_1700000000_cv.pdf"
    if (cleanRuta && cleanRuta.length > 0) {
      const url = `/api/v1/perfil/archivos/${cleanRuta}`;
      return this.sanitizer.bypassSecurityTrustResourceUrl(url);
    }
    return this.sanitizer.bypassSecurityTrustResourceUrl('');
  }

  /**
   * Genera URL de descarga para un archivo
   */
  obtenerUrlDescarga(ruta: string): string {
    // Manejar tanto rutas relativas como URLs completas
    let cleanRuta = ruta;
    
    // Si es una URL completa, extraer solo la ruta relativa
    if (ruta.startsWith('http://') || ruta.startsWith('https://')) {
      const url = new URL(ruta);
      const pathname = url.pathname;
      const match = pathname.match(/\/api\/v1\/perfil\/archivos\/(.+)/);
      if (match) {
        cleanRuta = match[1];
      }
    }
    
    const partes = cleanRuta.split('/');
    if (partes.length >= 2) {
      const tipo = partes[0];
      const filename = partes.slice(1).join('/');
      return `/api/v1/perfil/archivos/${tipo}/${filename}`;
    }
    return '';
  }
}




