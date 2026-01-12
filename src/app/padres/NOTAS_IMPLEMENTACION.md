# 🔧 NOTAS DE IMPLEMENTACIÓN - MÓDULO PADRES

## 📋 Lista de Control Pre-Implementación

### ✅ Frontend (Interfaces)

- [x] Todas las interfaces creadas
- [x] Servicio con métodos HTTP
- [x] Documentación completa
- [x] Ejemplo de componente
- [x] Tipos coherentes con BD

### ⏳ Backend (Pendiente)

- [ ] Validar schemas Pydantic
- [ ] Confirmar respuestas API
- [ ] Actualizar si es necesario
- [ ] Tests de API

### ⏳ Frontend (Componentes)

- [ ] Crear componentes standalone
- [ ] Implementar navegación
- [ ] Agregar formularios
- [ ] Estado global

---

## 🔄 Cambios Importantes a Tener en Cuenta

### 1. IDs Numéricos

**ANTES**: `id: string`
**AHORA**: `id: number`

```typescript
// En APIs que devuelven IDs
const hijoId: number = 1; // ✅ Correcto
const hijoId: string = '1'; // ❌ Incorrecto
```

### 2. Fechas en Formato ISO

**ANTES**: `fecha: Date`
**AHORA**: `fecha: string` (ISO 8601)

```typescript
// En respuesta API
"fecha": "2026-01-12"  // ✅ Correcto
"fecha": "12/01/2026"  // ❌ Incorrecto

// En componentes
const date = new Date("2026-01-12");  // ✅ Correcto
```

### 3. Arrays Obligatorios

**ANTES**: `pagos_pendientes: number` (suma)
**AHORA**: `pagosPendientes: PagoPendiente[]` (detalles)

```typescript
// En respuesta API
{
  "pagos_pendientes": [
    {
      "id": 1,
      "monto": 150000,
      "estado": "pendiente"
    }
  ]
}
```

### 4. Apellidos Separados

**ANTES**: `apellidos: string`
**AHORA**: `apellidoPaterno`, `apellidoMaterno`

```typescript
// En respuesta API
{
  "apellido_paterno": "García",
  "apellido_materno": "López"
}
```

---

## 🚨 Errores Comunes a Evitar

### Error 1: Usar `Date` en lugar de `string`

```typescript
// ❌ INCORRECTO
const data: InicioPage = {
  tarjetas: {
    proxSesion: {
      fecha: new Date(), // Type error!
    },
  },
};

// ✅ CORRECTO
const data: InicioPage = {
  tarjetas: {
    proxSesion: {
      fecha: '2026-01-12', // string
    },
  },
};
```

### Error 2: IDs como string

```typescript
// ❌ INCORRECTO
const hijoId = '123';
this.padresService.getHijoDetalle(hijoId);

// ✅ CORRECTO
const hijoId = 123;
this.padresService.getHijoDetalle(hijoId);

// O si viene como string:
const hijoId = parseInt('123', 10);
```

### Error 3: Olvidar null check

```typescript
// ❌ INCORRECTO
{{ inicioData.tarjetas.proxSesion.fecha }}

// ✅ CORRECTO
{{ inicioData.tarjetas.proxSesion?.fecha }}
{{ inicioData?.tarjetas?.proxSesion?.fecha }}

// O con *ngIf
<div *ngIf="inicioData?.tarjetas.proxSesion">
  {{ inicioData.tarjetas.proxSesion.fecha }}
</div>
```

### Error 4: No manejar arrays vacíos

```typescript
// ❌ INCORRECTO
{{ pagosPendientes[0].monto }}  // Error si array vacío

// ✅ CORRECTO
<div *ngIf="pagosPendientes.length > 0">
  {{ pagosPendientes[0].monto }}
</div>

// O con safe navigation
{{ pagosPendientes[0]?.monto }}
```

### Error 5: Formato de fecha incorrecto

```typescript
// ❌ INCORRECTO
{{ fecha }}  // "2026-01-12" sin formato

// ✅ CORRECTO
{{ fecha | date: 'fullDate' }}
{{ fecha | date: 'short' }}
{{ fecha | date: 'dd/MM/yyyy' }}
```

---

## 🎯 Guía de Implementación por Componente

### 1. Componente Inicio

**Estructura base**:

```typescript
export class InicioComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();
  inicioData: InicioPage | null = null;
  cargando = true;
  error: string | null = null;

  constructor(private padresService: PadresService) {}

  ngOnInit(): void {
    this.cargarDatos();
  }

  private cargarDatos(): void {
    this.padresService
      .getInicioData()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (respuesta) => {
          if (respuesta.exito) {
            this.inicioData = respuesta.datos;
          } else {
            this.error = respuesta.error;
          }
          this.cargando = false;
        },
        error: (err) => {
          this.error = 'Error de conexión';
          this.cargando = false;
        },
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

### 2. Componente Mis Hijos

**Similar a Inicio**, pero:

- Usar `getMisHijos()` en lugar de `getInicioData()`
- Manejar selección de hijo
- Usar `*ngFor` para listar hijos

### 3. Componente Sesiones

**Con filtros**:

```typescript
vistaActual: 'hoy' | 'programadas' | 'semana' = 'hoy';

cambiarVista(vista: typeof this.vistaActual) {
  this.vistaActual = vista;
  this.cargarSesiones();
}

private cargarSesiones() {
  this.padresService
    .getSesiones(this.vistaActual)
    .pipe(takeUntil(this.destroy$))
    .subscribe(...);
}
```

### 4. Componente Pagos

**Con tablas**:

- Usar `mat-table` o tabla HTML simple
- Formatear montos con currency pipe
- Colorear según estado

---

## 📱 Template Best Practices

### Carga de Datos

```html
<!-- Con spinner -->
<app-spinner *ngIf="cargando"></app-spinner>

<!-- Con datos -->
<div *ngIf="!cargando && inicioData">
  <!-- contenido -->
</div>

<!-- Con error -->
<div *ngIf="!cargando && error" class="error-banner">{{ error }}</div>
```

### Fechas

```html
<!-- Diferentes formatos -->
{{ fecha | date: 'fullDate' }} {{ fecha | date: 'shortDate' }} {{ fecha | date: 'shortTime' }} {{
fecha | date: 'medium' }} {{ fecha | date: 'yyyy-MM-dd' }}

<!-- Para español -->
<span [ngxDateFormat]="fecha" format="dd/MM/yyyy"></span>
```

### Montos

```html
<!-- Formateo de moneda -->
{{ monto | currency: 'COP':' ':'.2' }} {{ monto | currency: 'COP' }}

<!-- Con locale -->
{{ monto | number: '1.0-2' }}
```

### Condicionales

```html
<!-- Safe navigation -->
{{ datos?.tarjetas?.proxSesion?.fecha }}

<!-- Con *ngIf -->
<div *ngIf="datos?.tarjetas?.proxSesion">Hay próxima sesión</div>

<!-- Con else -->
<div *ngIf="datos?.tarjetas?.proxSesion; else noSesion">
  Próxima: {{ datos.tarjetas.proxSesion.fecha }}
</div>
<ng-template #noSesion> No hay próxima sesión programada </ng-template>
```

### Arrays

```html
<!-- Iteración simple -->
<div *ngFor="let pago of pagosPendientes">{{ pago.descripcion }}: {{ pago.monto | currency }}</div>

<!-- Con índice -->
<div *ngFor="let pago of pagosPendientes; let i = index">{{ i + 1 }}. {{ pago.descripcion }}</div>

<!-- Con track by -->
<div *ngFor="let pago of pagosPendientes; trackBy: trackByPagoId">{{ pago.descripcion }}</div>

// En componente: trackByPagoId(index: number, pago: PagoPendiente): number { return pago.id; }
```

---

## 🔌 Integración con Estado Global

### Con NgRx

```typescript
// Action
export const cargarInicio = createAction('[Padres] Cargar Inicio');

// Effect
cargarInicio$ = createEffect(() =>
  this.actions$.pipe(
    ofType(cargarInicio),
    switchMap(() => this.padresService.getInicioData()),
    map((respuesta) =>
      cargarInicioExito({
        datos: respuesta.datos,
      })
    )
  )
);

// Selector
export const selectInicioData = createSelector(selectPadresState, (state) => state.inicioData);
```

### Con Signals (Angular 17+)

```typescript
inicioData = signal<InicioPage | null>(null);
cargando = signal(true);
error = signal<string | null>(null);

constructor(private padresService: PadresService) {
  effect(() => {
    this.padresService.getInicioData().subscribe(
      respuesta => {
        if (respuesta.exito) {
          this.inicioData.set(respuesta.datos!);
        }
        this.cargando.set(false);
      }
    );
  });
}
```

---

## 🧪 Testing

### Test Unitario

```typescript
describe('InicioComponent', () => {
  let component: InicioComponent;
  let fixture: ComponentFixture<InicioComponent>;
  let padresService: jasmine.SpyObj<PadresService>;

  beforeEach(async () => {
    const padresServiceSpy = jasmine.createSpyObj('PadresService', ['getInicioData']);

    await TestBed.configureTestingModule({
      imports: [InicioComponent],
      providers: [{ provide: PadresService, useValue: padresServiceSpy }],
    }).compileComponents();

    padresService = TestBed.inject(PadresService) as jasmine.SpyObj<PadresService>;
  });

  it('debe cargar datos al iniciar', () => {
    const mockData: InicioPage = {
      saludo: 'Buenos días',
      hora: '09:00',
      hijoSeleccionado: { id: 1, nombre: 'Carlos' },
      hijosDisponibles: [],
      tarjetas: {
        proxSesion: null,
        ultimoAvance: null,
        pagosPendientes: [],
        documentosNuevos: [],
        ultimaObservacion: null,
      },
      cargando: false,
    };

    padresService.getInicioData.and.returnValue(
      of({
        exito: true,
        datos: mockData,
      })
    );

    fixture.detectChanges();

    expect(component.inicioData).toEqual(mockData);
    expect(component.cargando).toBe(false);
  });
});
```

---

## 🚀 Deployment Checklist

- [ ] Todas las interfaces importadas correctamente
- [ ] Tipos compilados sin errores
- [ ] Tests pasando > 80% coverage
- [ ] Documentación actualizada
- [ ] Componentes responsive
- [ ] Accesibilidad validada (a11y)
- [ ] Performance optimizada (lazy loading)
- [ ] Errores manejados apropiadamente
- [ ] Loading states implementados
- [ ] Cachéing estratégico

---

## 📚 Recursos Útiles

### Documentación Angular

- [Angular Docs](https://angular.io/docs)
- [RxJS Operators](https://rxjs.dev/api)
- [Angular Material](https://material.angular.io)

### Librerías Recomendadas

- `date-fns` - Manipulación de fechas
- `currency.js` - Cálculos monetarios
- `lodash` - Utilidades

### Testing

- [Testing Angular](https://angular.io/guide/testing)
- [Jasmine](https://jasmine.github.io)
- [Karma](https://karma-runner.github.io)

---

## ⚠️ Warnings a Considerar

1. **Memory Leaks**: Siempre desuscribirse con `takeUntil()`
2. **Null Safety**: Usar safe navigation operator `?.`
3. **Change Detection**: Considerar `OnPush` para performance
4. **CORS**: Validar que backend permita requests
5. **Cookies**: Si se usan para auth, configurar SameSite
6. **Dates**: Siempre trabajar con strings ISO, convertir cuando sea necesario

---

## 🎓 Training Path

1. **Semana 1**: Leer toda la documentación
2. **Semana 2**: Crear componente Inicio
3. **Semana 3**: Crear componentes Mis Hijos + Sesiones
4. **Semana 4**: Implementar estado global
5. **Semana 5**: Testing y optimización

---

**Versión**: 1.0
**Fecha**: 2026-01-12
**Estado**: ✅ Ready to Implement
