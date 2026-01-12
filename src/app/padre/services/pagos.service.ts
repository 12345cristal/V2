import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../enviroment/environment';
import {
  IPlan,
  IPago,
  IHistorialPagos,
  IMetodoPago
} from '../interfaces/pagos.interface';
import { IResponse, IResponsePaginado } from '../interfaces/shared.interface';

/**
 * Servicio para la gestión de pagos y planes
 * Proporciona métodos para manejar pagos, planes y facturación
 */
@Injectable({
  providedIn: 'root'
})
export class PagosService {
  private readonly baseUrl = `${environment.apiBaseUrl}/pagos`;

  constructor(private http: HttpClient) {}

  /**
   * Obtiene los planes activos del padre
   * @param padreId ID del padre
   * @returns Observable con la lista de planes
   */
  getPlanes(padreId: number): Observable<IPlan[]> {
    return this.http.get<IResponse<IPlan[]>>(`${this.baseUrl}/planes`, {
      params: new HttpParams().set('padreId', padreId.toString())
    }).pipe(
      map(response => response.data || []),
      catchError(this.handleError)
    );
  }

  /**
   * Obtiene un plan por su ID
   * @param planId ID del plan
   * @returns Observable con el plan
   */
  getPlan(planId: number): Observable<IPlan> {
    return this.http.get<IResponse<IPlan>>(`${this.baseUrl}/planes/${planId}`)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene el historial de pagos
   * @param padreId ID del padre
   * @param ninoId ID del niño (opcional)
   * @param page Número de página
   * @param pageSize Tamaño de página
   * @returns Observable con los pagos paginados
   */
  getHistorialPagos(
    padreId: number,
    ninoId?: number,
    page: number = 1,
    pageSize: number = 20
  ): Observable<IResponsePaginado<IPago>> {
    let params = new HttpParams()
      .set('padreId', padreId.toString())
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    if (ninoId) {
      params = params.set('ninoId', ninoId.toString());
    }

    return this.http.get<IResponsePaginado<IPago>>(this.baseUrl, { params })
      .pipe(catchError(this.handleError));
  }

  /**
   * Obtiene el resumen de pagos de un niño
   * @param ninoId ID del niño
   * @returns Observable con el historial completo de pagos
   */
  getHistorialCompleto(ninoId: number): Observable<IHistorialPagos> {
    return this.http.get<IResponse<IHistorialPagos>>(`${this.baseUrl}/historial/${ninoId}`)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Obtiene un pago por su ID
   * @param pagoId ID del pago
   * @returns Observable con el pago
   */
  getPago(pagoId: number): Observable<IPago> {
    return this.http.get<IResponse<IPago>>(`${this.baseUrl}/${pagoId}`)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Registra un nuevo pago
   * @param pago Datos del pago
   * @returns Observable con el pago registrado
   */
  registrarPago(pago: Partial<IPago>): Observable<IPago> {
    return this.http.post<IResponse<IPago>>(this.baseUrl, pago)
      .pipe(
        map(response => response.data!),
        catchError(this.handleError)
      );
  }

  /**
   * Sube un comprobante de pago
   * @param pagoId ID del pago
   * @param archivo Archivo del comprobante
   * @returns Observable con el pago actualizado
   */
  subirComprobante(pagoId: number, archivo: File): Observable<IPago> {
    const formData = new FormData();
    formData.append('comprobante', archivo);

    return this.http.post<IResponse<IPago>>(
      `${this.baseUrl}/${pagoId}/comprobante`,
      formData
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Obtiene los pagos pendientes del padre
   * @param padreId ID del padre
   * @returns Observable con la lista de pagos pendientes
   */
  getPagosPendientes(padreId: number): Observable<IPago[]> {
    return this.http.get<IResponse<IPago[]>>(`${this.baseUrl}/pendientes`, {
      params: new HttpParams().set('padreId', padreId.toString())
    }).pipe(
      map(response => response.data || []),
      catchError(this.handleError)
    );
  }

  /**
   * Descarga un recibo de pago
   * @param pagoId ID del pago
   * @returns Observable con el blob del PDF
   */
  descargarRecibo(pagoId: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/${pagoId}/recibo`, {
      responseType: 'blob'
    }).pipe(catchError(this.handleError));
  }

  /**
   * Solicita factura de un pago
   * @param pagoId ID del pago
   * @param datosFacturacion Datos para la factura
   * @returns Observable con la confirmación
   */
  solicitarFactura(
    pagoId: number,
    datosFacturacion: {
      rfc: string;
      razonSocial: string;
      usoCFDI: string;
      email: string;
    }
  ): Observable<void> {
    return this.http.post<IResponse<void>>(
      `${this.baseUrl}/${pagoId}/factura`,
      datosFacturacion
    ).pipe(
      map(() => undefined),
      catchError(this.handleError)
    );
  }

  /**
   * Configura renovación automática de un plan
   * @param planId ID del plan
   * @param activar Si es true activa la renovación, si es false la desactiva
   * @returns Observable con el plan actualizado
   */
  configurarRenovacionAutomatica(planId: number, activar: boolean): Observable<IPlan> {
    return this.http.patch<IResponse<IPlan>>(
      `${this.baseUrl}/planes/${planId}/renovacion`,
      { renovacionAutomatica: activar }
    ).pipe(
      map(response => response.data!),
      catchError(this.handleError)
    );
  }

  /**
   * Maneja los errores HTTP
   * @param error Error HTTP
   * @returns Observable con el error
   */
  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'Ocurrió un error desconocido';
    
    if (error.error instanceof ErrorEvent) {
      errorMessage = `Error: ${error.error.message}`;
    } else {
      errorMessage = error.error?.message || `Error del servidor: ${error.status}`;
    }
    
    console.error('Error en PagosService:', errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
