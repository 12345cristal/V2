import { Component, signal, inject, effect } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DocumentosPadreService } from '../../services/documentos-padre.service';
import { DocumentoPadre } from '../../interfaces/documento.interface';

@Component({
  selector: 'app-documentos-padre',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './documentos.component.html',
  styleUrls: ['./documentos.component.scss'],
})
export class DocumentosPadreComponent {

  private service = inject(DocumentosPadreService);

  hijoId = signal<number | null>(null);
  documentos = signal<DocumentoPadre[]>([]);
  cargando = signal(false);

  constructor() {
    effect(() => {
      if (this.hijoId()) {
        this.cargar();
      }
    });
  }

  cargar(): void {
    const id = this.hijoId();
    if (!id) return;

    this.cargando.set(true);
    this.service.getDocumentos(id).subscribe({
      next: (docs: DocumentoPadre[]) => {
        this.documentos.set(docs);
        this.cargando.set(false);
      },
      error: (error: unknown) => {
        console.error('Error cargando documentos:', error);
        this.cargando.set(false);
      }
    });
  }

  ver(doc: DocumentoPadre): void {
    if (!doc.visto) {
      this.service.marcarVisto(doc.id).subscribe({
        next: () => {
          // Actualizar el documento localmente
          const docs = this.documentos();
          const index = docs.findIndex(d => d.id === doc.id);
          if (index !== -1) {
            docs[index].visto = true;
            this.documentos.set([...docs]);
          }
        },
        error: (error: unknown) => {
          console.error('Error marcando visto:', error);
        }
      });
    }
    this.service.descargar(doc.url, doc.nombre);
  }
}
