// src/app/terapeuta/service/dashboard-terapeuta.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  DashboardTerapeuta,
  SesionDelDia,
  NinoAsignadoHoy,
  TareaRecurso,
  NotificacionDashboard,
  EstadisticasSemanales
} from '../interfaces/inicio-terapeuta.interface';

@Injectable({ providedIn: 'root' })
export class DashboardTerapeutaService {
  private apiUrl = `${environment.apiBaseUrl}/inicio`;


  constructor(private http: HttpClient) {}

  // 🔵 Versión real con backend
  getDashboard(): Observable<DashboardTerapeuta> {
  return this.http.get<DashboardTerapeuta>(this.apiUrl);
}

  // 🧪 Versión MOCK para probar sin backend
  getDashboardMock(): Observable<DashboardTerapeuta> {
    const hoy = 'Viernes, 28 de noviembre de 2025';

    const sesionesDelDia: SesionDelDia[] = [
      {
        id_sesion: 1,
        id_nino: 101,
        nombre_nino: 'Luis Torres',
        fotografia: 'https://via.placeholder.com/64',
        terapia: 'Terapia de Lenguaje',
        sala: 'Sala 2',
        es_reposicion: true,
        hora_inicio: '09:00',
        hora_fin: '09:45',
        nota_importante: 'Viene sensible a ruidos hoy.'
      },
      {
        id_sesion: 2,
        id_nino: 102,
        nombre_nino: 'Ana Ruiz',
        fotografia: 'https://via.placeholder.com/64',
        terapia: 'Terapia Conductual',
        sala: 'Sala 1',
        es_reposicion: false,
        hora_inicio: '10:00',
        hora_fin: '10:45'
      },
      {
        id_sesion: 3,
        id_nino: 103,
        nombre_nino: 'Mateo López',
        fotografia: 'https://via.placeholder.com/64',
        terapia: 'Psicología',
        sala: 'Sala 3',
        es_reposicion: false,
        hora_inicio: '11:00',
        hora_fin: '11:45',
        nota_importante: 'Revisar cambios de conducta en casa.',
        tiene_retraso: true
      }
    ];

    const ninosAsignadosHoy: NinoAsignadoHoy[] = [
      {
        id_nino: 101,
        nombre: 'Luis Torres',
        fotografia: 'https://via.placeholder.com/56',
        terapiaPrincipal: 'Lenguaje',
        proximoHorario: '09:00 - 09:45',
        ultimasSesiones: [
          {
            fecha: '2025-11-21',
            terapia: 'Lenguaje',
            resumen: 'Trabajó bien en imitación de sonidos.'
          },
          {
            fecha: '2025-11-14',
            terapia: 'Lenguaje',
            resumen: 'Mejora en contacto visual.'
          },
          {
            fecha: '2025-11-07',
            terapia: 'Lenguaje',
            resumen: 'Se mostró inquieto al inicio.'
          }
        ],
        ultimaNotaClinica: 'Priorizar ejercicios de articulación y respiración.',
        progresoGeneral: 'Mejorando',
        indicadores: {
          conducta: 72,
          comunicacion: 65,
          sensorial: 55,
          autonomia: 40
        }
      },
      {
        id_nino: 102,
        nombre: 'Ana Ruiz',
        fotografia: 'https://via.placeholder.com/56',
        terapiaPrincipal: 'Conductual',
        proximoHorario: '10:00 - 10:45',
        ultimasSesiones: [
          {
            fecha: '2025-11-20',
            terapia: 'Conductual',
            resumen: 'Se logró disminuir berrinches a la mitad.'
          }
        ],
        ultimaNotaClinica: 'Mantener rutina previa a sesión, responde bien.',
        progresoGeneral: 'Estable',
        indicadores: {
          conducta: 60,
          comunicacion: 50,
          sensorial: 48,
          autonomia: 38
        }
      }
    ];

    const tareasPendientes: TareaRecurso[] = [
      {
        recurso: 'Imitación motora básica',
        totalAsignados: 3,
        completados: 1      },
      {
        recurso: 'Rutina de relajación antes de dormir',
        totalAsignados: 2,
        completados: 0
      }
    ];

    const notificaciones: NotificacionDashboard[] = [
      {
        mensaje: 'Se asignó reposición para Luis Torres el día de hoy.',
        fecha: '2025-11-28T08:15:00',
        tipo: 'reposicion'
      },
      {
        mensaje: 'Cambio de horario de Ana Ruiz para la próxima semana.',
        fecha: '2025-11-27T18:00:00',
        tipo: 'cambio-horario'
      },
      {
        mensaje: 'La mamá de Mateo subió un documento nuevo.',
        fecha: '2025-11-27T16:30:00',
        tipo: 'documento'
      }
    ];

    const estadisticasSemanales: EstadisticasSemanales = {
      totalSesiones: 18,
      asistenciasCompletadas: 15,
      cancelaciones: 2,
      reposicionesPendientes: 3,
      satisfaccionPromedio: 4.6
    };

    const dashboard: DashboardTerapeuta = {
      terapeuta: {
        id_terapeuta: 1,
        nombre: 'Dra. Carolina Méndez',
        especialidad: 'Terapia de Lenguaje',
        estadoLaboral: 'ACTIVO',
        fechaHoy: hoy
      },
      resumen: {
        sesionesHoy: 6,
        reposiciones: 1,
        tareasPendientes: 2
      },
      sesionesDelDia,
      ninosAsignadosHoy,
      tareasPendientes,
      notificaciones,
      estadisticasSemanales
    };

    return of(dashboard);
  }
}




