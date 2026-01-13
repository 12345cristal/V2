// src/app/coordinador/prioridad-ninos/prioridad-ninos.ts
import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TopsisService } from '../../service/topsis.service';
import { NinosService } from '../../service/ninos.service';
import { 
  CriterioTopsis, 
  TopsisInput, 
  TopsisResultado 
} from '../../interfaces/topsis.interface';

interface NinoConDatos {
  id: number;
  nombre_completo: string;
  valores: number[];
}

/**
 * Componente para cálculo de prioridad de niños usando TOPSIS
 * Solo accesible para rol COORDINADOR
 */
@Component({
  selector: 'app-prioridad-ninos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './prioridad-ninos.html',
  styleUrls: ['./prioridad-ninos.scss']
})
export class PrioridadNinosComponent implements OnInit {
  // Signals para estado reactivo
  criterios = signal<CriterioTopsis[]>([]);
  ninos = signal<NinoConDatos[]>([]);
  resultados = signal<TopsisResultado[]>([]);
  cargando = signal<boolean>(false);
  cargandoCriterios = signal<boolean>(false);
  cargandoNinos = signal<boolean>(false);
  mensajeError = signal<string>('');
  mensajeExito = signal<string>('');
  mensajeAdvertencia = signal<string>('');

  // Estados del componente
  mostrarFormCriterio = false;
  criterioEditando: CriterioTopsis | null = null;
  nuevoCriterio: CriterioTopsis = {
    nombre: '',
    descripcion: '',
    peso: 0.25,
    tipo: 'beneficio',
    activo: 1
  };
  
  // Validaciones
  errorValidacion = signal<string>('');

  constructor(
    private topsisService: TopsisService,
    private ninosService: NinosService
  ) {}

  ngOnInit(): void {
    this.cargarCriterios();
    this.cargarNinos();
  }

  /**
   * Carga los criterios TOPSIS desde el backend
   */
  cargarCriterios(): void {
    this.cargandoCriterios.set(true);
    this.mensajeError.set('');
    
    this.topsisService.getCriteriosTopsis(false).subscribe({
      next: (data) => {
        this.criterios.set(data);
        this.cargandoCriterios.set(false);
        
        if (data.length === 0) {
          this.mensajeAdvertencia.set('⚠️ No hay criterios configurados. Por favor, cree al menos uno para comenzar.');
        } else {
          this.validarSumaPesos(data);
          this.inicializarMatriz();
        }
      },
      error: (error) => {
        const mensaje = error.error?.detail || error.message || 'Error desconocido';
        this.mensajeError.set(`❌ Error al cargar criterios: ${mensaje}`);
        this.cargandoCriterios.set(false);
      }
    });
  }
  
  /**
   * Valida que la suma de pesos sea 1.0
   */
  validarSumaPesos(criterios: CriterioTopsis[]): void {
    const sumaPesos = criterios.reduce((sum, c) => sum + c.peso, 0);
    const diferencia = Math.abs(sumaPesos - 1.0);
    
    if (diferencia > 0.01) {
      this.mensajeAdvertencia.set(
        `⚠️ Advertencia: La suma de pesos es ${sumaPesos.toFixed(2)}. Se recomienda que sea exactamente 1.0 para resultados óptimos.`
      );
    } else {
      this.mensajeAdvertencia.set('');
    }
  }

  /**
   * Carga los niños activos desde el backend
   */
  cargarNinos(): void {
    this.cargandoNinos.set(true);
    this.mensajeError.set('');
    
    this.ninosService.getNinos().subscribe({
      next: (data: any[]) => {
        const ninosActivos = data.filter((n: any) => n.estado === 'ACTIVO');
        
        const ninosConDatos: NinoConDatos[] = ninosActivos.map((n: any) => ({
          id: n.id,
          nombre_completo: `${n.nombre} ${n.apellido_paterno} ${n.apellido_materno || ''}`.trim(),
          valores: [] // Se llenará manualmente o se inicializará con la matriz
        }));
        
        this.ninos.set(ninosConDatos);
        this.cargandoNinos.set(false);
        
        if (ninosConDatos.length === 0) {
          this.mensajeAdvertencia.set('⚠️ No hay niños activos en el sistema. Registre niños para poder evaluarlos.');
        } else {
          this.inicializarMatriz();
        }
      },
      error: (error: any) => {
        const mensaje = error.error?.detail || error.message || 'Error desconocido';
        this.mensajeError.set(`❌ Error al cargar niños: ${mensaje}`);
        this.cargandoNinos.set(false);
      }
    });
  }

  /**
   * Inicializa la matriz de valores para los niños según los criterios
   */
  inicializarMatriz(): void {
    const numCriterios = this.criterios().length;
    this.ninos.update(ninos => 
      ninos.map(n => ({
        ...n,
        valores: n.valores.length === numCriterios 
          ? n.valores 
          : new Array(numCriterios).fill(0)
      }))
    );
  }

  /**
   * Calcula la prioridad usando TOPSIS
   */
  calcularPrioridad(): void {
    // Limpiar mensajes previos
    this.mensajeError.set('');
    this.mensajeExito.set('');
    this.mensajeAdvertencia.set('');
    this.errorValidacion.set('');
    
    const criteriosList = this.criterios();
    const ninosList = this.ninos();

    // Validaciones
    if (criteriosList.length === 0) {
      this.mensajeError.set('❌ Debe configurar al menos un criterio antes de calcular.');
      return;
    }

    if (ninosList.length === 0) {
      this.mensajeError.set('❌ No hay niños activos para evaluar.');
      return;
    }
    
    if (ninosList.length < 2) {
      this.mensajeAdvertencia.set('⚠️ Se recomienda evaluar al menos 2 niños para obtener rankings significativos.');
    }

    // Validar que todos los valores estén completos
    const matrizCompleta = ninosList.every(nino => 
      nino.valores.length === criteriosList.length && 
      nino.valores.every(v => v !== null && v !== undefined && !isNaN(v))
    );
    
    if (!matrizCompleta) {
      this.mensajeError.set('❌ Complete todos los valores de la matriz antes de calcular. Todos los campos deben tener valores numéricos.');
      return;
    }
    
    // Validar que haya variación en los datos
    const hayVariacion = criteriosList.some((_, colIndex) => {
      const valores = ninosList.map(n => n.valores[colIndex]);
      const min = Math.min(...valores);
      const max = Math.max(...valores);
      return max !== min;
    });
    
    if (!hayVariacion) {
      this.mensajeAdvertencia.set('⚠️ Todos los niños tienen los mismos valores. Los resultados pueden no ser significativos.');
    }

    // Preparar input para TOPSIS
    const input: TopsisInput = {
      ids: ninosList.map(n => n.id),
      matriz: ninosList.map(n => n.valores)
    };

    this.cargando.set(true);
    
    this.topsisService.calcularPrioridadNinos(input).subscribe({
      next: (resultados) => {
        this.resultados.set(resultados);
        this.cargando.set(false);
        
        const numNinos = resultados.length;
        this.mensajeExito.set(
          `✅ Análisis TOPSIS completado exitosamente para ${numNinos} ${numNinos === 1 ? 'niño' : 'niños'}. Los resultados se ordenaron por prioridad.`
        );
        
        // Limpiar mensaje después de 5 segundos
        setTimeout(() => this.mensajeExito.set(''), 5000);
        
        // Scroll a resultados
        setTimeout(() => {
          const resultSection = document.querySelector('.seccion-resultados');
          resultSection?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
      },
      error: (error) => {
        const detalle = error.error?.detail || error.message || 'Error desconocido al comunicarse con el servidor';
        this.mensajeError.set(`❌ Error al calcular prioridad: ${detalle}`);
        this.cargando.set(false);
        console.error('Error TOPSIS:', error);
      }
    });
  }

  /**
   * Obtiene el nombre del niño por su ID
   */
  getNombreNino(ninoId: number): string {
    const nino = this.ninos().find(n => n.id === ninoId);
    return nino ? nino.nombre_completo : `Niño ${ninoId}`;
  }

  /**
   * Abre el formulario para crear un nuevo criterio
   */
  abrirFormCriterio(): void {
    this.mostrarFormCriterio = true;
    this.criterioEditando = null;
    this.nuevoCriterio = {
      nombre: '',
      descripcion: '',
      peso: 0.25,
      tipo: 'beneficio',
      activo: 1
    };
  }

  /**
   * Guarda un criterio (crear o actualizar)
   */
  guardarCriterio(): void {
    // Limpiar mensajes
    this.errorValidacion.set('');
    this.mensajeError.set('');
    
    // Validaciones
    if (!this.nuevoCriterio.nombre || this.nuevoCriterio.nombre.trim() === '') {
      this.errorValidacion.set('❌ El nombre del criterio es obligatorio');
      return;
    }
    
    if (this.nuevoCriterio.nombre.length < 3) {
      this.errorValidacion.set('❌ El nombre debe tener al menos 3 caracteres');
      return;
    }
    
    if (this.nuevoCriterio.peso <= 0 || this.nuevoCriterio.peso > 1) {
      this.errorValidacion.set('❌ El peso debe estar entre 0.01 y 1.00');
      return;
    }
    
    // Validar nombre duplicado (excepto si está editando el mismo)
    const nombreDuplicado = this.criterios().some(c => 
      c.nombre.toLowerCase() === this.nuevoCriterio.nombre.trim().toLowerCase() &&
      c.id !== this.criterioEditando?.id
    );
    
    if (nombreDuplicado) {
      this.errorValidacion.set('❌ Ya existe un criterio con ese nombre');
      return;
    }

    this.cargando.set(true);

    if (this.criterioEditando && this.criterioEditando.id) {
      // Actualizar
      this.topsisService.updateCriterioTopsis(
        this.criterioEditando.id, 
        this.nuevoCriterio
      ).subscribe({
        next: () => {
          this.cargarCriterios();
          this.cerrarFormCriterio();
          this.mensajeExito.set(`✅ Criterio "${this.nuevoCriterio.nombre}" actualizado exitosamente`);
          setTimeout(() => this.mensajeExito.set(''), 4000);
        },
        error: (error) => {
          const mensaje = error.error?.detail || error.message || 'Error desconocido';
          this.mensajeError.set(`❌ Error al actualizar criterio: ${mensaje}`);
          this.cargando.set(false);
        }
      });
    } else {
      // Crear
      this.topsisService.createCriterioTopsis(this.nuevoCriterio).subscribe({
        next: () => {
          this.cargarCriterios();
          this.cerrarFormCriterio();
          this.mensajeExito.set(`✅ Criterio "${this.nuevoCriterio.nombre}" creado exitosamente`);
          setTimeout(() => this.mensajeExito.set(''), 4000);
        },
        error: (error) => {
          const mensaje = error.error?.detail || error.message || 'Error desconocido';
          this.mensajeError.set(`❌ Error al crear criterio: ${mensaje}`);
          this.cargando.set(false);
        }
      });
    }
  }

  /**
   * Edita un criterio existente
   */
  editarCriterio(criterio: CriterioTopsis): void {
    this.criterioEditando = criterio;
    this.nuevoCriterio = { ...criterio };
    this.mostrarFormCriterio = true;
  }

  /**
   * Elimina un criterio
   */
  eliminarCriterio(id: number | undefined): void {
    if (!id) return;
    
    const criterio = this.criterios().find(c => c.id === id);
    const nombreCriterio = criterio?.nombre || 'este criterio';
    
    if (!confirm(`¿Está seguro de eliminar el criterio "${nombreCriterio}"?\n\n⚠️ Esta acción no se puede deshacer y afectará los cálculos futuros.`)) {
      return;
    }

    this.cargando.set(true);
    this.mensajeError.set('');
    
    this.topsisService.deleteCriterioTopsis(id).subscribe({
      next: () => {
        this.cargarCriterios();
        this.resultados.set([]); // Limpiar resultados anteriores
        this.mensajeExito.set(`✅ Criterio "${nombreCriterio}" eliminado exitosamente`);
        setTimeout(() => this.mensajeExito.set(''), 4000);
      },
      error: (error) => {
        const mensaje = error.error?.detail || error.message || 'Error desconocido';
        this.mensajeError.set(`❌ Error al eliminar criterio: ${mensaje}`);
        this.cargando.set(false);
      }
    });
  }

  /**
   * Cierra el formulario de criterio
   */
  cerrarFormCriterio(): void {
    this.mostrarFormCriterio = false;
    this.criterioEditando = null;
    this.errorValidacion.set('');
  }
  
  /**
   * Obtiene la suma total de pesos
   */
  getSumaPesos(): number {
    return this.criterios().reduce((sum, c) => sum + c.peso, 0);
  }
  
  /**
   * Verifica si la suma de pesos es correcta
   */
  isSumaPesosCorrecta(): boolean {
    return Math.abs(this.getSumaPesos() - 1.0) <= 0.01;
  }
  
  // Exponer Math para el template
  Math = Math;
}

