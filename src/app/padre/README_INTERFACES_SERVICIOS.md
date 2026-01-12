# Padre Dashboard - Interfaces y Servicios

Este documento describe la estructura completa de interfaces TypeScript y servicios Angular creados para el módulo Padre (Dashboard).

## 📁 Estructura de Archivos

```
src/app/padre/
├── interfaces/
│   ├── index.ts                    # Exportaciones centralizadas
│   ├── dashboard.interface.ts      # 6 interfaces para dashboard
│   ├── mis-hijos.interface.ts      # 4 interfaces para gestión de hijos
│   ├── sesiones.interface.ts       # 5 interfaces + 2 enums para sesiones
│   ├── historial.interface.ts      # 4 interfaces para historial
│   ├── tareas.interface.ts         # 3 interfaces + 1 enum para tareas
│   ├── pagos.interface.ts          # 4 interfaces + 1 enum para pagos
│   ├── documentos.interface.ts     # 2 interfaces + 1 enum para documentos
│   ├── recursos.interface.ts       # 2 interfaces + 1 enum para recursos
│   ├── mensajes.interface.ts       # 3 interfaces + 1 enum para mensajería
│   ├── notificaciones.interface.ts # 3 interfaces + 2 enums para notificaciones
│   ├── perfil.interface.ts         # 3 interfaces para perfil y configuración
│   └── shared.interface.ts         # 6 interfaces comunes
├── services/
│   ├── index.ts                    # Exportaciones centralizadas
│   ├── padre.service.ts            # Servicio principal
│   ├── sesiones.service.ts         # Gestión de sesiones
│   ├── pagos.service.ts            # Gestión de pagos
│   ├── documentos.service.ts       # Gestión de documentos
│   ├── mensajes.service.ts         # Sistema de mensajería
│   ├── recursos.service.ts         # Recursos educativos
│   └── tareas.service.ts           # Gestión de tareas
├── padre.module.ts                 # Módulo principal
└── padre-routing.module.ts         # Configuración de rutas
```

## 📊 Interfaces Principales

### 1. Dashboard (dashboard.interface.ts)
- `IDashboardResumen`: Resumen general del dashboard
- `IProximaSesion`: Información de próxima sesión
- `IUltimoAvance`: Último avance del niño
- `IPagosPendientes`: Pagos pendientes
- `IDocumentoNuevo`: Documentos nuevos
- `IObservacionTerapeuta`: Observaciones del terapeuta

### 2. Mis Hijos (mis-hijos.interface.ts)
- `IHijo`: Información completa del hijo
- `IAlergias`: Alergias del niño
- `IMedicamento`: Medicamentos
- `IEstadoMedicamento`: Estados de medicamentos (enum)

### 3. Sesiones (sesiones.interface.ts)
- `ISesion`: Sesión terapéutica completa
- `ITipoTerapia`: Tipos de terapia (enum)
- `IEstadoSesion`: Estados de sesión (enum)
- `IBitacoraDaily`: Bitácora diaria
- `IGrabacionVoz`: Grabaciones de voz

### 4. Historial (historial.interface.ts)
- `IHistorialTerapeutico`: Historial completo
- `IAsistenciaMes`: Asistencia mensual
- `IEvolucionObjetivos`: Evolución de objetivos
- `IGrafica`: Datos para gráficas

### 5. Tareas (tareas.interface.ts)
- `ITarea`: Tarea asignada
- `IEstadoTarea`: Estados de tarea (enum)
- `IRecursoAsociado`: Recursos de la tarea

### 6. Pagos (pagos.interface.ts)
- `IPlan`: Plan contratado
- `IPago`: Registro de pago
- `IHistorialPagos`: Historial completo
- `IMetodoPago`: Métodos de pago (enum)

### 7. Documentos (documentos.interface.ts)
- `IDocumento`: Documento del sistema
- `ITipoDocumento`: Tipos de documento (enum)

### 8. Recursos (recursos.interface.ts)
- `IRecurso`: Recurso educativo
- `ITipoRecurso`: Tipos de recurso (enum)

### 9. Mensajes (mensajes.interface.ts)
- `IChat`: Conversación
- `IMensaje`: Mensaje individual
- `ITipoChat`: Tipos de chat (enum)

### 10. Notificaciones (notificaciones.interface.ts)
- `INotificacion`: Notificación del sistema
- `ITipoNotificacion`: Tipos de notificación (enum)
- `IEstadoNotificacion`: Estados de notificación (enum)

### 11. Perfil (perfil.interface.ts)
- `IPerfilPadre`: Perfil completo del padre
- `IAccesibilidad`: Configuración de accesibilidad
- `IPreferenciasUsuario`: Preferencias del usuario

### 12. Compartidas (shared.interface.ts)
- `IUsuario`: Usuario del sistema
- `ITerapeuta`: Información del terapeuta
- `ICoordinador`: Información del coordinador
- `IAdministrador`: Información del administrador
- `IResponse<T>`: Respuesta genérica del API
- `IPaginacion`: Configuración de paginación

## 🔧 Servicios

### PadreService
Servicio principal para gestión del módulo padre.

**Métodos principales:**
```typescript
getDashboardResumen(padreId: number): Observable<IDashboardResumen>
getProximaSesion(padreId: number): Observable<IProximaSesion | null>
getUltimoAvance(padreId: number): Observable<IUltimoAvance | null>
getPagosPendientes(padreId: number): Observable<IPagosPendientes[]>
getDocumentosNuevos(padreId: number): Observable<IDocumentoNuevo[]>
getObservacionesTerapeuta(padreId: number, pendientesOnly?: boolean): Observable<IObservacionTerapeuta[]>
getHijos(padreId: number, activos?: boolean): Observable<IHijo[]>
getHijo(hijoId: number): Observable<IHijo>
actualizarHijo(hijoId: number, data: Partial<IHijo>): Observable<IHijo>
```

### SesionesService
Gestión de sesiones terapéuticas.

**Métodos principales:**
```typescript
getSesiones(padreId: number, filtros?, page?, pageSize?): Observable<IResponsePaginado<ISesion>>
getSesion(sesionId: number): Observable<ISesion>
confirmarAsistencia(sesionId: number): Observable<ISesion>
cancelarSesion(sesionId: number, motivo: string): Observable<ISesion>
solicitarReprogramacion(sesionId: number, nuevaFecha: string, motivo: string): Observable<void>
getBitacora(sesionId: number): Observable<IBitacoraDaily | null>
getGrabaciones(sesionId: number): Observable<IGrabacionVoz[]>
getProximasSesiones(padreId: number, limit?: number): Observable<ISesion[]>
getHistorialSesiones(ninoId: number, page?, pageSize?): Observable<IResponsePaginado<ISesion>>
```

### PagosService
Gestión de pagos y planes.

**Métodos principales:**
```typescript
getPlanes(padreId: number): Observable<IPlan[]>
getPlan(planId: number): Observable<IPlan>
getHistorialPagos(padreId: number, ninoId?, page?, pageSize?): Observable<IResponsePaginado<IPago>>
getHistorialCompleto(ninoId: number): Observable<IHistorialPagos>
getPago(pagoId: number): Observable<IPago>
registrarPago(pago: Partial<IPago>): Observable<IPago>
subirComprobante(pagoId: number, archivo: File): Observable<IPago>
getPagosPendientes(padreId: number): Observable<IPago[]>
descargarRecibo(pagoId: number): Observable<Blob>
solicitarFactura(pagoId: number, datosFacturacion): Observable<void>
configurarRenovacionAutomatica(planId: number, activar: boolean): Observable<IPlan>
```

### DocumentosPadreService
Gestión de documentos.

**Métodos principales:**
```typescript
getDocumentos(padreId: number, filtros?, page?, pageSize?): Observable<IResponsePaginado<IDocumento>>
getDocumento(documentoId: number): Observable<IDocumento>
subirDocumento(data, archivo: File): Observable<IDocumento>
actualizarDocumento(documentoId: number, data: Partial<IDocumento>): Observable<IDocumento>
eliminarDocumento(documentoId: number): Observable<void>
descargarDocumento(documentoId: number): Observable<Blob>
marcarComoVisto(documentoId: number): Observable<IDocumento>
archivarDocumento(documentoId: number): Observable<IDocumento>
buscarDocumentos(termino: string, padreId: number): Observable<IDocumento[]>
```

### MensajesService
Sistema de mensajería.

**Métodos principales:**
```typescript
getChats(usuarioId: number, filtros?): Observable<IChat[]>
getChat(chatId: number): Observable<IChat>
crearChat(data): Observable<IChat>
getMensajes(chatId: number, page?, pageSize?): Observable<IResponsePaginado<IMensaje>>
enviarMensaje(chatId: number, contenido: string, adjuntos?, respondidoAId?): Observable<IMensaje>
editarMensaje(mensajeId: number, nuevoContenido: string): Observable<IMensaje>
eliminarMensaje(mensajeId: number, paraTodos?: boolean): Observable<void>
marcarComoLeidos(chatId: number): Observable<void>
silenciarChat(chatId: number, silenciar: boolean): Observable<IChat>
archivarChat(chatId: number, archivar: boolean): Observable<IChat>
buscarMensajes(chatId: number, termino: string): Observable<IMensaje[]>
```

### RecursosService
Gestión de recursos educativos.

**Métodos principales:**
```typescript
getRecursos(filtros?, page?, pageSize?): Observable<IResponsePaginado<IRecurso>>
getRecurso(recursoId: number): Observable<IRecurso>
getRecursosRecomendados(ninoId: number, limit?: number): Observable<IRecurso[]>
marcarFavorito(recursoId: number, usuarioId: number): Observable<IRecurso>
quitarFavorito(recursoId: number, usuarioId: number): Observable<IRecurso>
marcarCompletado(recursoId: number, usuarioId: number, progreso?: number): Observable<IRecurso>
actualizarProgreso(recursoId: number, usuarioId: number, progreso: number): Observable<IRecurso>
calificarRecurso(recursoId: number, usuarioId: number, calificacion: number): Observable<IRecurso>
registrarAccion(recursoId: number, tipo: 'visualizacion' | 'descarga'): Observable<void>
agregarNotas(recursoId: number, usuarioId: number, notas: string): Observable<IRecurso>
buscarRecursos(termino: string): Observable<IRecurso[]>
getCategorias(): Observable<string[]>
```

### TareasService
Gestión de tareas asignadas.

**Métodos principales:**
```typescript
getTareas(padreId: number, filtros?, page?, pageSize?): Observable<IResponsePaginado<ITarea>>
getTarea(tareaId: number): Observable<ITarea>
completarTarea(tareaId: number, comentarios?: string): Observable<ITarea>
reportarProgreso(tareaId: number, progreso): Observable<ITarea>
getTareasPendientes(padreId: number, limit?: number): Observable<ITarea[]>
getTareasVencidas(padreId: number): Observable<ITarea[]>
configurarNotificaciones(tareaId: number, activar: boolean): Observable<ITarea>
getHistorialTareas(ninoId: number, page?, pageSize?): Observable<IResponsePaginado<ITarea>>
descargarRecurso(recursoId: number): Observable<Blob>
```

## 🚀 Uso

### Importar Interfaces
```typescript
// Importar interfaces específicas
import { IDashboardResumen, IProximaSesion } from '@app/padre/interfaces/dashboard.interface';

// O importar todas desde el index
import { IDashboardResumen, IProximaSesion, ISesion } from '@app/padre/interfaces';
```

### Importar Servicios
```typescript
// Importar servicios específicos
import { PadreService } from '@app/padre/services/padre.service';

// O importar todos desde el index
import { PadreService, SesionesService } from '@app/padre/services';
```

### Usar en Componentes
```typescript
import { Component, OnInit } from '@angular/core';
import { PadreService } from '@app/padre/services';
import { IDashboardResumen } from '@app/padre/interfaces';

@Component({
  selector: 'app-dashboard',
  template: `...`
})
export class DashboardComponent implements OnInit {
  resumen?: IDashboardResumen;

  constructor(private padreService: PadreService) {}

  ngOnInit() {
    this.padreService.getDashboardResumen(1).subscribe(
      resumen => this.resumen = resumen
    );
  }
}
```

## 📝 Características

- ✅ **Tipado fuerte**: Todas las interfaces están completamente tipadas
- ✅ **Documentación JSDoc**: Todos los métodos públicos documentados
- ✅ **Manejo de errores**: Error handling consistente en todos los servicios
- ✅ **Paginación**: Soporte para paginación en endpoints que lo requieren
- ✅ **Filtros**: Capacidad de filtrado en listados
- ✅ **CRUD completo**: Operaciones Create, Read, Update, Delete donde aplica
- ✅ **Subida de archivos**: Soporte para FormData en documentos y comprobantes
- ✅ **Descarga de archivos**: Métodos para descargar PDFs, recibos, etc.
- ✅ **Enums**: Estados y tipos definidos como enums para type safety
- ✅ **Interfaces compartidas**: Reutilización de interfaces comunes

## 🔐 Seguridad

- ✅ Sin vulnerabilidades detectadas (CodeQL)
- ✅ Manejo seguro de archivos
- ✅ Validación de tipos en tiempo de compilación
- ✅ Headers HTTP correctos para archivos

## 📦 Módulos

### PadreModule
Módulo principal que agrupa todos los servicios y configuraciones.

### PadreRoutingModule
Define las rutas para las 11 secciones del dashboard:
1. Dashboard / Inicio
2. Mis Hijos
3. Sesiones
4. Historial Terapéutico
5. Tareas / Actividades
6. Pagos
7. Documentos
8. Recursos Educativos
9. Mensajes
10. Notificaciones
11. Perfil y Configuración

## 🛠️ Mantenimiento

Para agregar nuevas interfaces o servicios:

1. Crear el archivo en el directorio correspondiente
2. Seguir las convenciones de nomenclatura existentes
3. Agregar documentación JSDoc
4. Actualizar el archivo index.ts correspondiente
5. Ejecutar pruebas de TypeScript

## 📚 Referencias

- [Angular HttpClient](https://angular.io/guide/http)
- [TypeScript Interfaces](https://www.typescriptlang.org/docs/handbook/interfaces.html)
- [RxJS Observables](https://rxjs.dev/guide/observable)
