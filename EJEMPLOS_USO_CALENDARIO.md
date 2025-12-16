# 💼 EJEMPLOS PRÁCTICOS DE USO - SISTEMA DE CITAS CON GOOGLE CALENDAR

## 📋 CASO DE USO 1: Programar sesión semanal de terapia

### Escenario
El coordinador necesita programar sesiones de terapia de lenguaje para Juan Pérez, todos los lunes a las 10:00 AM durante un mes.

### Solución con el Sistema

```http
### 1. Crear primera sesión
POST http://localhost:8000/api/v1/citas-calendario/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "nino_id": 5,
  "terapeuta_id": 3,
  "terapia_id": 2,
  "fecha": "2025-12-23",
  "hora_inicio": "10:00:00",
  "hora_fin": "11:00:00",
  "estado_id": 1,
  "motivo": "Sesión semanal de terapia de lenguaje",
  "sincronizar_google_calendar": true
}

### 2. Crear segunda sesión (30/12)
POST http://localhost:8000/api/v1/citas-calendario/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "nino_id": 5,
  "terapeuta_id": 3,
  "terapia_id": 2,
  "fecha": "2025-12-30",
  "hora_inicio": "10:00:00",
  "hora_fin": "11:00:00",
  "estado_id": 1,
  "motivo": "Sesión semanal de terapia de lenguaje",
  "sincronizar_google_calendar": true
}

### 3. Y así sucesivamente...
```

**Resultado:**
- ✅ 4 citas creadas en BD
- ✅ 4 eventos en Google Calendar
- ✅ Notificaciones automáticas configuradas
- ✅ Coordinador puede ver todas en el calendario

---

## 🔄 CASO DE USO 2: Reprogramar cita por enfermedad

### Escenario
Juan Pérez se enfermó el 23/12. El coordinador debe reprogramar su cita del lunes al miércoles 25/12.

```http
### Reprogramar cita ID 42
PUT http://localhost:8000/api/v1/citas-calendario/42/reprogramar
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "nueva_fecha": "2025-12-25",
  "nueva_hora_inicio": "10:00:00",
  "nueva_hora_fin": "11:00:00",
  "motivo": "Niño enfermo el 23/12, reprogramado para el 25/12",
  "actualizar_google_calendar": true
}
```

**Resultado:**
- ✅ Cita actualizada en BD
- ✅ Evento actualizado en Google Calendar
- ✅ Nueva notificación enviada automáticamente
- ✅ Historial de cambios guardado en `observaciones`

**Verificar:**
```http
GET http://localhost:8000/api/v1/citas-calendario/42
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## ❌ CASO DE USO 3: Cancelar cita por emergencia familiar

### Escenario
La familia de Juan tuvo una emergencia el 30/12. Deben cancelar la cita y no pueden reprogramar aún.

```http
### Cancelar cita ID 43
PUT http://localhost:8000/api/v1/citas-calendario/43/cancelar
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "motivo_cancelacion": "Emergencia familiar. La familia salió de la ciudad inesperadamente.",
  "eliminar_de_google_calendar": true,
  "crear_reposicion": false
}
```

**Resultado:**
- ✅ Estado cambiado a `CANCELADA`
- ✅ Evento eliminado de Google Calendar
- ✅ Auditoría completa:
  - `cancelado_por`: ID del coordinador
  - `fecha_cancelacion`: 2025-12-16 14:30:00
  - `motivo_cancelacion`: Guardado en BD

---

## 📅 CASO DE USO 4: Consultar calendario del terapeuta

### Escenario
El coordinador quiere ver todas las citas del terapeuta ID 3 en diciembre para programar nuevas sesiones.

```http
### Ver calendario de terapeuta
GET http://localhost:8000/api/v1/citas-calendario/calendario?fecha_inicio=2025-12-01&fecha_fin=2025-12-31&terapeuta_id=3
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Respuesta:**
```json
[
  {
    "id_cita": 42,
    "nino_id": 5,
    "terapeuta_id": 3,
    "terapia_id": 2,
    "fecha": "2025-12-25",
    "hora_inicio": "10:00:00",
    "hora_fin": "11:00:00",
    "estado_id": 1,
    "google_calendar_link": "https://www.google.com/calendar/event?eid=...",
    "sincronizado_calendar": true,
    "confirmada": false
  },
  {
    "id_cita": 44,
    "nino_id": 7,
    "terapeuta_id": 3,
    "terapia_id": 1,
    "fecha": "2025-12-26",
    "hora_inicio": "14:00:00",
    "hora_fin": "15:00:00",
    "estado_id": 1,
    "google_calendar_link": "https://www.google.com/calendar/event?eid=...",
    "sincronizado_calendar": true,
    "confirmada": true
  }
]
```

**Uso:**
- Ver horarios disponibles del terapeuta
- Evitar conflictos de horarios
- Planificar nuevas citas

---

## 👨‍👩‍👧 CASO DE USO 5: Ver citas de un niño específico

### Escenario
La mamá de Juan pregunta cuándo son las próximas sesiones de su hijo.

```http
### Ver citas de Juan (ID 5) en diciembre
GET http://localhost:8000/api/v1/citas-calendario/calendario?nino_id=5&fecha_inicio=2025-12-01&fecha_fin=2025-12-31
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Resultado:**
```json
[
  {
    "id_cita": 42,
    "nino_id": 5,
    "fecha": "2025-12-25",
    "hora_inicio": "10:00:00",
    "terapia_id": 2,
    "google_calendar_link": "https://..."
  },
  {
    "id_cita": 45,
    "nino_id": 5,
    "fecha": "2025-12-27",
    "hora_inicio": "15:00:00",
    "terapia_id": 1,
    "google_calendar_link": "https://..."
  }
]
```

---

## 🔍 CASO DE USO 6: Verificar citas confirmadas

### Escenario
El coordinador quiere ver solo las citas que ya han sido confirmadas por los padres.

```http
### Ver solo citas confirmadas
GET http://localhost:8000/api/v1/citas-calendario/calendario?solo_confirmadas=true&fecha_inicio=2025-12-01
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🔧 CASO DE USO 7: Debugging - Verificar sincronización

### Escenario
Una cita se creó pero no aparece en Google Calendar. El coordinador necesita verificar el estado.

```http
### Ver detalles completos de la cita
GET http://localhost:8000/api/v1/citas-calendario/42
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Respuesta:**
```json
{
  "id_cita": 42,
  "nino_id": 5,
  "terapeuta_id": 3,
  "terapia_id": 2,
  "fecha": "2025-12-25",
  "hora_inicio": "10:00:00",
  "hora_fin": "11:00:00",
  "google_event_id": "abc123xyz789",
  "google_calendar_link": "https://www.google.com/calendar/event?eid=abc123xyz789",
  "sincronizado_calendar": true,  ← ✅ SINCRONIZADO
  "fecha_sincronizacion": "2025-12-16T14:30:00",
  "confirmada": false,
  "fecha_creacion": "2025-12-16T14:30:00",
  "creado_por": 2
}
```

**Diagnóstico:**
- `sincronizado_calendar: true` → Evento creado exitosamente
- `google_event_id` → Tiene ID válido
- `google_calendar_link` → Link funcional para abrir directamente

**Si sincronizado_calendar es false:**
1. Verificar logs del backend
2. Verificar credenciales de Google
3. Verificar que el calendario esté compartido

---

## 📊 CASO DE USO 8: Generar reporte semanal

### Escenario
El coordinador necesita un reporte de todas las citas de la semana.

```http
### Citas de la semana del 23-29 de diciembre
GET http://localhost:8000/api/v1/citas-calendario/calendario?fecha_inicio=2025-12-23&fecha_fin=2025-12-29
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Procesamiento en Frontend:**
```typescript
// Angular service
obtenerReporteSemanal(): Observable<ReporteSemanal> {
  return this.http.get<CitaResponse[]>(
    `${this.baseUrl}/calendario?fecha_inicio=2025-12-23&fecha_fin=2025-12-29`
  ).pipe(
    map(citas => {
      const por_dia = this.agruparPorDia(citas);
      const por_terapeuta = this.agruparPorTerapeuta(citas);
      const total = citas.length;
      const confirmadas = citas.filter(c => c.confirmada).length;
      const canceladas = citas.filter(c => c.estado_id === ESTADO_CANCELADA).length;
      
      return {
        por_dia,
        por_terapeuta,
        total,
        confirmadas,
        canceladas,
        tasa_confirmacion: (confirmadas / total) * 100
      };
    })
  );
}
```

---

## 🚀 CASO DE USO 9: Integración con frontend (Angular)

### Service Completo

```typescript
// src/app/service/citas-calendario.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface CitaCreate {
  nino_id: number;
  terapeuta_id: number;
  terapia_id: number;
  fecha: string; // YYYY-MM-DD
  hora_inicio: string; // HH:MM:SS
  hora_fin: string;
  estado_id: number;
  motivo?: string;
  sincronizar_google_calendar: boolean;
}

export interface CitaResponse {
  id_cita: number;
  nino_id: number;
  terapeuta_id: number;
  terapia_id: number;
  fecha: string;
  hora_inicio: string;
  hora_fin: string;
  google_event_id?: string;
  google_calendar_link?: string;
  sincronizado_calendar: boolean;
  confirmada: boolean;
}

@Injectable({ providedIn: 'root' })
export class CitasCalendarioService {
  private baseUrl = 'http://localhost:8000/api/v1/citas-calendario';

  constructor(private http: HttpClient) {}

  crearCita(cita: CitaCreate): Observable<CitaResponse> {
    return this.http.post<CitaResponse>(`${this.baseUrl}/`, cita);
  }

  reprogramarCita(
    id: number,
    nueva_fecha: string,
    nueva_hora_inicio: string,
    nueva_hora_fin: string,
    motivo?: string
  ): Observable<CitaResponse> {
    return this.http.put<CitaResponse>(
      `${this.baseUrl}/${id}/reprogramar`,
      {
        nueva_fecha,
        nueva_hora_inicio,
        nueva_hora_fin,
        motivo,
        actualizar_google_calendar: true
      }
    );
  }

  cancelarCita(id: number, motivo: string): Observable<CitaResponse> {
    return this.http.put<CitaResponse>(
      `${this.baseUrl}/${id}/cancelar`,
      {
        motivo_cancelacion: motivo,
        eliminar_de_google_calendar: true,
        crear_reposicion: false
      }
    );
  }

  obtenerCalendario(filtros: {
    fecha_inicio?: string;
    fecha_fin?: string;
    terapeuta_id?: number;
    nino_id?: number;
    solo_confirmadas?: boolean;
  }): Observable<CitaResponse[]> {
    let params = new HttpParams();
    
    if (filtros.fecha_inicio) params = params.set('fecha_inicio', filtros.fecha_inicio);
    if (filtros.fecha_fin) params = params.set('fecha_fin', filtros.fecha_fin);
    if (filtros.terapeuta_id) params = params.set('terapeuta_id', filtros.terapeuta_id.toString());
    if (filtros.nino_id) params = params.set('nino_id', filtros.nino_id.toString());
    if (filtros.solo_confirmadas) params = params.set('solo_confirmadas', 'true');
    
    return this.http.get<CitaResponse[]>(`${this.baseUrl}/calendario`, { params });
  }

  obtenerDetalle(id: number): Observable<CitaResponse> {
    return this.http.get<CitaResponse>(`${this.baseUrl}/${id}`);
  }
}
```

### Componente de ejemplo

```typescript
// src/app/coordinador/calendario-citas/calendario-citas.component.ts
import { Component, OnInit } from '@angular/core';
import { CitasCalendarioService, CitaResponse } from '../../service/citas-calendario.service';

@Component({
  selector: 'app-calendario-citas',
  templateUrl: './calendario-citas.component.html'
})
export class CalendarioCitasComponent implements OnInit {
  citas: CitaResponse[] = [];
  cargando = false;

  constructor(private citasService: CitasCalendarioService) {}

  ngOnInit() {
    this.cargarCalendario();
  }

  cargarCalendario() {
    this.cargando = true;
    const hoy = new Date();
    const fin_mes = new Date(hoy.getFullYear(), hoy.getMonth() + 1, 0);

    this.citasService.obtenerCalendario({
      fecha_inicio: hoy.toISOString().split('T')[0],
      fecha_fin: fin_mes.toISOString().split('T')[0]
    }).subscribe({
      next: (citas) => {
        this.citas = citas;
        this.cargando = false;
      },
      error: (error) => {
        console.error('Error al cargar calendario', error);
        this.cargando = false;
      }
    });
  }

  abrirEnGoogleCalendar(cita: CitaResponse) {
    if (cita.google_calendar_link) {
      window.open(cita.google_calendar_link, '_blank');
    }
  }

  reprogramar(cita: CitaResponse) {
    // Mostrar modal para reprogramar
    // ...
  }

  cancelar(cita: CitaResponse) {
    const motivo = prompt('Motivo de cancelación:');
    if (motivo) {
      this.citasService.cancelarCita(cita.id_cita, motivo).subscribe({
        next: () => {
          alert('Cita cancelada exitosamente');
          this.cargarCalendario();
        },
        error: (error) => alert('Error al cancelar: ' + error.error.detail)
      });
    }
  }
}
```

---

## 🧪 CASO DE USO 10: Testing con Postman Collection

### Importar en Postman

```json
{
  "info": {
    "name": "Citas Calendario API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000/api/v1"
    },
    {
      "key": "token",
      "value": "TU_TOKEN_AQUI"
    }
  ],
  "item": [
    {
      "name": "1. Login Coordinador",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/auth/login",
        "body": {
          "mode": "raw",
          "raw": "{\"email\":\"coordinador@test.com\",\"password\":\"123456\"}"
        }
      }
    },
    {
      "name": "2. Crear Cita",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/citas-calendario/",
        "header": [
          {"key": "Authorization", "value": "Bearer {{token}}"}
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"nino_id\":1,\"terapeuta_id\":2,\"terapia_id\":1,\"fecha\":\"2025-12-25\",\"hora_inicio\":\"10:00:00\",\"hora_fin\":\"11:00:00\",\"sincronizar_google_calendar\":true}"
        }
      }
    },
    {
      "name": "3. Ver Calendario",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/citas-calendario/calendario?fecha_inicio=2025-12-01",
        "header": [
          {"key": "Authorization", "value": "Bearer {{token}}"}
        ]
      }
    }
  ]
}
```

---

**Estos ejemplos cubren el 95% de los casos de uso comunes en un centro terapéutico.**
