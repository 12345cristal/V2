import { Component, OnInit, signal, computed, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RecursosService } from '../../services/recursos.service';
import { AuthService } from '../../services/auth.service';

interface Recurso {
  id: number;
  titulo: string;
  descripcion: string;
  tipo_recurso: 'PDF' | 'VIDEO' | 'ENLACE';
  categoria_recurso: string;
  nivel_recurso: string;
  url: string;
  archivo: string | null;
  objetivo_terapeutico: string;
  terapeuta_nombre: string;
  fecha_creacion: string;
  visto: boolean;
}

interface RecursosPorTerapeuta {
  terapeuta: string;
  recursos: Recurso[];
}

@Component({
  selector: 'app-recursos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './recursos.component.html',
  styleUrls: ['./recursos.component.scss']
})
export class RecursosComponent implements OnInit {
  recursos = signal<Recurso[]>([]);
  cargando = signal<boolean>(true);
  error = signal<string | null>(null);
  filtroTipo = signal<string>('TODOS');
  filtroVisto = signal<string>('TODOS');

  recursosFiltrados = computed(() => {
    let filtrados = this.recursos();
    
    if (this.filtroTipo() !== 'TODOS') {
      filtrados = filtrados.filter(r => r.tipo_recurso === this.filtroTipo());
    }
    
    if (this.filtroVisto() === 'VISTO') {
      filtrados = filtrados.filter(r => r.visto);
    } else if (this.filtroVisto() === 'NO_VISTO') {
      filtrados = filtrados.filter(r => !r.visto);
    }
    
    return filtrados;
  });

  recursosPorTerapeuta = computed(() => {
    const agrupados = new Map<string, Recurso[]>();
    
    this.recursosFiltrados().forEach(recurso => {
      const terapeuta = recurso.terapeuta_nombre;
      if (!agrupados.has(terapeuta)) {
        agrupados.set(terapeuta, []);
      }
      agrupados.get(terapeuta)!.push(recurso);
    });
    
    const resultado: RecursosPorTerapeuta[] = [];
    agrupados.forEach((recursos, terapeuta) => {
      resultado.push({ terapeuta, recursos });
    });
    
    return resultado;
  });

  recursosNoVistos = computed(() => 
    this.recursos().filter(r => !r.visto).length
  );

  constructor(
    private recursosService: RecursosService,
    private authService: AuthService
  ) {
    effect(() => {
      console.log(`Recursos no vistos: ${this.recursosNoVistos()}`);
    });
  }

  ngOnInit(): void {
    this.cargarRecursos();
  }

  cargarRecursos(): void {
    this.cargando.set(true);
    this.error.set(null);

    this.recursosService.obtenerRecursosRecomendados().subscribe({
      next: (datos) => {
        this.recursos.set(datos);
        this.cargando.set(false);
      },
      error: (err) => {
        this.error.set('Error al cargar los recursos. Por favor, intenta de nuevo.');
        this.cargando.set(false);
        console.error('Error:', err);
      }
    });
  }

  abrirRecurso(recurso: Recurso): void {
    if (!recurso.visto) {
      this.marcarComoVisto(recurso.id);
    }

    if (recurso.tipo_recurso === 'PDF' && recurso.archivo) {
      window.open(recurso.archivo, '_blank');
    } else if (recurso.tipo_recurso === 'VIDEO' || recurso.tipo_recurso === 'ENLACE') {
      window.open(recurso.url, '_blank');
    }
  }

  descargarRecurso(recurso: Recurso, event: Event): void {
    event.stopPropagation();
    
    if (!recurso.visto) {
      this.marcarComoVisto(recurso.id);
    }

    if (recurso.archivo) {
      const link = document.createElement('a');
      link.href = recurso.archivo;
      link.download = recurso.titulo;
      link.click();
    }
  }

  marcarComoVisto(recursoId: number): void {
    this.recursosService.marcarComoVisto(recursoId).subscribe({
      next: () => {
        this.recursos.update(recursos => 
          recursos.map(r => r.id === recursoId ? { ...r, visto: true } : r)
        );
      },
      error: (err) => {
        console.error('Error al marcar como visto:', err);
      }
    });
  }

  cambiarFiltroTipo(tipo: string): void {
    this.filtroTipo.set(tipo);
  }

  cambiarFiltroVisto(estado: string): void {
    this.filtroVisto.set(estado);
  }

  getIconoTipo(tipo: string): string {
    switch (tipo) {
      case 'PDF': return '📄';
      case 'VIDEO': return '🎥';
      case 'ENLACE': return '🔗';
      default: return '📋';
    }
  }

  getColorCategoria(categoria: string): string {
    const colores: { [key: string]: string } = {
      'Comunicación': 'azul',
      'Social': 'verde',
      'Conducta': 'naranja',
      'Sensorial': 'morado',
      'Cognitivo': 'rosa'
    };
    return colores[categoria] || 'gris';
  }
}
