# 🎯 Arquitectura con Signals - Guía Técnica

## ¿Qué son Signals?

Angular Signals es una nueva API para reactividad que reemplaza:
- RxJS Subjects/BehaviorSubjects
- Observable properties
- ChangeDetectionStrategy manual

**Ventajas:**
- ✅ Más simple y directo
- ✅ Mejor performance
- ✅ Type-safe
- ✅ Menos boilerplate

---

## 📊 Comparación: Antes vs Después

### ❌ ANTES (Clase tradicional)
```typescript
export class TerapiasComponent {
  terapias: Terapia[] = [];
  personalDisponible: Personal[] = [];
  personalAsignado: Personal[] = [];
  cargando = false;
  filtroSexo = 'todos';
  filtroTerapia = 'todos';

  constructor(private service: TerapiaService) {}

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.cargando = true;
    this.service.getTerapias().subscribe(data => {
      this.terapias = data;
      this.cargando = false;
    });
  }

  aplicarFiltros() {
    // Lógica de filtrado manual, sin reactividad
  }
}
```

**Problemas:**
- ❌ Propiedades mutables
- ❌ Cambios no son reactivos automáticamente
- ❌ Mucho código boilerplate
- ❌ Difícil de debuggear

---

### ✅ DESPUÉS (Con Signals)

```typescript
export class TerapiasComponent {
  // Signals simples
  terapias = signal<Terapia[]>([]);
  personalDisponible = signal<Personal[]>([]);
  personalAsignado = signal<Personal[]>([]);
  cargando = signal(false);
  filtroSexo = signal('todos');
  filtroTerapia = signal('todos');
  busqueda = signal('');

  // Computed: reactividad automática
  personalAsignadoFiltrado = computed(() => {
    const personal = this.personalAsignado();
    const sexo = this.filtroSexo();
    const terapia = this.filtroTerapia();
    const busca = this.busqueda();

    return personal.filter(p => {
      const coincideSexo = sexo === 'todos' || p.sexo === sexo;
      const coincideTerapia = terapia === 'todos' || p.id_terapia === terapia;
      const coincideBusca = p.nombres.includes(busca);
      
      return coincideSexo && coincideTerapia && coincideBusca;
    });
  });

  constructor(private service: TerapiaService = inject(TerapiaService)) {}

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.cargando.set(true);
    this.service.getTerapias().subscribe(data => {
      this.terapias.set(data);
      this.cargando.set(false);
    });
  }

  cambiarFiltroSexo(sexo: string) {
    this.filtroSexo.set(sexo);
    // personalAsignadoFiltrado se actualiza AUTOMÁTICAMENTE
  }
}
```

**Ventajas:**
- ✅ Sintaxis clara y concisa
- ✅ Filtros se actualizan automáticamente
- ✅ No necesitas suscripciones
- ✅ Type-safe
- ✅ Mejor performance (OnPush strategy)

---

## 🔧 API de Signals

### 1. `signal()` - Crear un Signal

```typescript
// Signal simple
const count = signal(0);
const nombre = signal('Juan');
const activo = signal(true);

// Signal con tipo
const usuarios = signal<Usuario[]>([]);
const datos = signal<DatosCompletos | null>(null);

// Signal con inicializador
const items = signal(() => {
  console.log('Inicializando...');
  return [1, 2, 3];
});
```

### 2. `.set()` - Actualizar un Signal

```typescript
// Actualizar valor completo
count.set(5);
nombre.set('María');
usuarios.set(dataFromAPI);

// No usar esto en Angular Signals:
// ❌ this.count.value = 5;
// ❌ this.usuarios = newData;
```

### 3. `.update()` - Actualizar basado en valor anterior

```typescript
// Incrementar contador
count.update(c => c + 1);

// Agregar a lista
usuarios.update(lista => [...lista, nuevoUsuario]);

// Cambiar propiedad
persona.update(p => ({ ...p, email: 'nuevo@email.com' }));
```

### 4. `.mutate()` - Mutar objetos complejos (cuidado)

```typescript
// USAR CON CUIDADO - para cambios internos de arrays/objetos
usuarios.mutate(lista => {
  lista.push(nuevoUsuario);
});

// Preferir .update():
usuarios.update(lista => [...lista, nuevoUsuario]);
```

### 5. `computed()` - Derivar valores reactivamente

```typescript
// Computed que depende de signals
const totalActivos = computed(() => {
  return usuarios().filter(u => u.estado === 'ACTIVO').length;
});

// Nested computed
const estadisticas = computed(() => {
  return {
    total: usuarios().length,
    activos: totalActivos(),
    inactivos: usuarios().length - totalActivos()
  };
});

// En template:
// {{ estadisticas().activos }}
```

### 6. `effect()` - Ejecutar código cuando signals cambien

```typescript
// Ejecutar acción cuando contador cambia
effect(() => {
  console.log('Contador ahora es:', count());
  // Guardar en localStorage
  localStorage.setItem('count', count().toString());
});

// Ejecutar cuando usuario cambia
effect(() => {
  const usuario = usuarioActual();
  if (usuario) {
    console.log('Usuario cambió a:', usuario.nombre);
    this.cargarPermisos(usuario.id);
  }
});
```

---

## 📝 Patrones Comunes

### Patrón 1: Cargar datos del servidor

```typescript
export class PersonasComponent {
  personas = signal<Persona[]>([]);
  cargando = signal(false);
  error = signal<string | null>(null);

  constructor(private service = inject(PersonaService)) {}

  ngOnInit() {
    this.cargarDatos();
  }

  cargarDatos() {
    this.cargando.set(true);
    this.error.set(null);

    this.service.getPersonas().subscribe({
      next: (datos) => {
        this.personas.set(datos);
        this.cargando.set(false);
      },
      error: (err) => {
        this.error.set('Error al cargar');
        this.cargando.set(false);
      }
    });
  }
}
```

### Patrón 2: Filtrado reactivo

```typescript
export class ListaComponent {
  items = signal<Item[]>([]);
  filtroNombre = signal('');
  filtroCategoria = signal('todos');
  filtroActivos = signal(true);

  // Computed que filtra automáticamente
  itemsFiltrados = computed(() => {
    const items = this.items();
    const nombre = this.filtroNombre().toLowerCase();
    const categoria = this.filtroCategoria();
    const soloActivos = this.filtroActivos();

    return items.filter(item => {
      const coincideNombre = item.nombre.toLowerCase().includes(nombre);
      const coincideCategoria = categoria === 'todos' || item.categoria === categoria;
      const coincideEstado = !soloActivos || item.activo;

      return coincideNombre && coincideCategoria && coincideEstado;
    });
  });

  // En template:
  // <input (input)="filtroNombre.set($event.target.value)" />
  // {{ itemsFiltrados().length }} resultados
}
```

### Patrón 3: Formularios reactivos + Signals

```typescript
export class FormComponent {
  form = signal(new FormGroup({
    nombre: new FormControl('', Validators.required),
    email: new FormControl('', [Validators.required, Validators.email])
  }));

  enviando = signal(false);
  resultado = signal<ResultadoGuardar | null>(null);

  guardar() {
    if (this.form().invalid) return;

    this.enviando.set(true);
    const datos = this.form().value;

    this.service.guardar(datos).subscribe({
      next: (res) => {
        this.resultado.set(res);
        this.enviando.set(false);
      },
      error: (err) => {
        this.resultado.set({ error: 'Fallo' });
        this.enviando.set(false);
      }
    });
  }
}
```

### Patrón 4: Estado global simple

```typescript
// store.service.ts
export class StoreService {
  usuarioActual = signal<Usuario | null>(null);
  temaOscuro = signal(false);
  notificaciones = signal<Notificacion[]>([]);

  setUsuario(usuario: Usuario) {
    this.usuarioActual.set(usuario);
  }

  toggleTema() {
    this.temaOscuro.update(v => !v);
  }

  agregarNotificacion(notif: Notificacion) {
    this.notificaciones.update(lista => [...lista, notif]);
  }
}

// En componente:
export class MiComponente {
  private store = inject(StoreService);
  
  usuario = this.store.usuarioActual;
  tema = this.store.temaOscuro;
  notificaciones = this.store.notificaciones;

  // En template:
  // {{ usuario()?.nombre }}
  // [class.dark]="tema()"
}
```

---

## 🎯 Uso en Templates

### Leer un Signal
```html
<!-- Necesitas () para leer el valor -->
<p>Nombre: {{ nombre() }}</p>
<p>Total: {{ personas().length }}</p>
<p>Activos: {{ estadisticas().activos }}</p>
```

### Directivas con Signals
```html
<!-- *ngIf -->
@if (cargando()) {
  <p>Cargando...</p>
} @else {
  <div>Contenido cargado</div>
}

<!-- *ngFor -->
@for (persona of personas(); track persona.id) {
  <div>{{ persona.nombre }}</div>
}

<!-- Condicional con else-if -->
@if (estado() === 'cargando') {
  <p>Cargando...</p>
} @else if (estado() === 'error') {
  <p>Error</p>
} @else {
  <p>{{ datos() }}</p>
}
```

### Property Binding
```html
<input [value]="nombre()" (input)="nombre.set($event.target.value)" />
<button [disabled]="cargando()" (click)="guardar()">Guardar</button>
<div [class.activo]="activo()">Activo</div>
<div [style.color]="tema() === 'oscuro' ? '#fff' : '#000'">Texto</div>
```

---

## ⚡ Performance con OnPush

Signals trabaja mejor con `ChangeDetectionStrategy.OnPush`:

```typescript
@Component({
  selector: 'app-ejemplo',
  template: `...`,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class EjemploComponent {
  // Solo detecta cambios en:
  // 1. Inputs cambien
  // 2. Signals cambien
  // 3. Eventos DOM
  // No revisa toda la jerarquía
}
```

**Resultado:** ⚡ Aplicación más rápida

---

## 🚫 Qué NO hacer con Signals

```typescript
// ❌ NO HACER
const personas = signal<Persona[]>([]);

// Agregar modificando el array
personas().push(nuevoPersona); // ❌ INCORRECTO

// Cambiar propiedad interna
personas()[0].nombre = 'Juan'; // ❌ INCORRECTO

// ✅ CORRECTO

// Usar .set()
personas.set([...personas(), nuevoPersona]);

// Usar .update()
personas.update(lista => [...lista, nuevoPersona]);

// Para cambiar propiedad:
personas.mutate(lista => {
  lista[0].nombre = 'Juan';
});
// O mejor:
personas.update(lista => 
  lista.map((p, i) => i === 0 ? { ...p, nombre: 'Juan' } : p)
);
```

---

## 📊 Signals en los Componentes Nuevos

### TerapiasComponent
```typescript
// Signals básicos
terapias = signal<Terapia[]>([]);
personalDisponible = signal<Personal[]>([]);
personalAsignado = signal<Personal[]>([]);
filtroSexo = signal<'todos' | 'M' | 'F'>('todos');
filtroTerapia = signal<number | 'todos'>('todos');
busqueda = signal('');

// Computed (se actualiza automáticamente)
personalAsignadoFiltrado = computed(() => {
  // Filtra personal cuando algún filtro cambia
});
```

### PerfilComponent
```typescript
// Signals básicos
datosPersonales = signal<DatosCompletos | null>(null);
cargando = signal(false);
tabActiva = signal<'datos' | 'documentos' | 'seguridad'>('datos');
editandoDatos = signal(false);

// Computed (alertas inteligentes)
documentosFaltantes = computed(() => {
  // Detecta automáticamente qué documentos faltan
});

completitud = computed(() => {
  // Calcula porcentaje de perfil completado
});
```

---

## 🔄 Ciclo de Vida con Signals

```typescript
export class MiComponent implements OnInit {
  datos = signal<Datos | null>(null);
  cargando = signal(false);

  constructor(private service = inject(MiService)) {}

  ngOnInit() {
    // 1. Componente se crea
    // 2. Signals se inicializan con valores por defecto
    // 3. ngOnInit se ejecuta
    
    this.cargar();
  }

  cargar() {
    // 4. Cambias un signal
    this.cargando.set(true);
    
    // 5. El template se actualiza automáticamente
    // @if (cargando()) { <spinner /> }
    
    // 6. Cuando llegan datos, actualizas otro signal
    this.service.obtener().subscribe(data => {
      this.datos.set(data);
      this.cargando.set(false);
      // Template se actualiza de nuevo
    });
  }

  ngOnDestroy() {
    // Los signals se destruyen con el componente
    // No necesitas desuscribirse de observables
    // si usas signals con takeUntilDestroyed()
  }
}
```

---

## 📚 Recursos Importantes

### Documentación oficial
- https://angular.io/guide/signals

### Ejemplos en el proyecto
- `src/app/coordinador/terapias/terapias.ts` - Ejemplo completo
- `src/app/perfil/perfil.ts` - Otro ejemplo

### Migration guide (de RxJS a Signals)
```typescript
// Antes (RxJS)
usuarios$ = this.service.getUsuarios().pipe(
  startWith([]),
  shareReplay(1)
);

// Después (Signals)
usuarios = signal<Usuario[]>([]);

ngOnInit() {
  this.service.getUsuarios().subscribe(data => {
    this.usuarios.set(data);
  });
}
```

---

## ✅ Checklist de Implementación

Al crear un componente con Signals:

- [ ] Importar `signal`, `computed`, `effect`, `inject`
- [ ] Declarar signals como propiedades públicas
- [ ] Usar `.set()` para actualizar valores
- [ ] Usar `computed()` para valores derivados
- [ ] Usar `ChangeDetectionStrategy.OnPush`
- [ ] En templates, llamar signals con `()`
- [ ] Usar `@if`, `@for` en lugar de `*ngIf`, `*ngFor`
- [ ] Limpiar con `effect()` si necesitas side effects
- [ ] No usar `ngOnChanges` ni `ChangeDetectorRef.detectChanges()`

---

**¡Signals hacen el código más limpio y performante! 🚀**
