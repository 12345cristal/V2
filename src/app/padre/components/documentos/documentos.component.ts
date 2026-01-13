import { Component, OnInit, signal } from '@angular/core';
import { DocumentosService } from '../../../service/documentos.service';
import { DocumentoPadre } from '../../../interfaces/documento.interface';

@Component({
  selector: 'app-documentos',
  templateUrl: './documentos.component.html',
  styleUrls: ['./documentos.component.scss']
})
export class DocumentosComponent implements OnInit {
  // IDs de contexto
  usuarioId: number = 1;
  hijoId: number | null = null;

  // Estado con señales (coincide con el uso de .set y ())
  documentos = signal<DocumentoPadre[]>([]);
  cargando = signal<boolean>(false);
  mostrarFormulario = signal<boolean>(false);
  archivoSeleccionado = signal<File | null>(null);

  constructor(private documentosService: DocumentosService) {}

  ngOnInit(): void {
    this.cargarDocumentos();
  }

  cargarDocumentos(tipo?: string): void {
    this.cargando.set(true);
    this.documentosService.getDocumentos(this.usuarioId, tipo).subscribe({
      next: (docs: DocumentoPadre[]) => {
        this.documentos.set(docs);
        this.cargando.set(false);
      },
      error: () => this.cargando.set(false)
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = (input.files && input.files[0]) ? input.files[0] : null;
    this.archivoSeleccionado.set(file);
  }

  subirDocumento(): void {
    const file = this.archivoSeleccionado();
    if (!file) return;

    this.cargando.set(true);
    this.documentosService.subir(file, this.usuarioId, file.name).subscribe({
      next: (response: DocumentoPadre) => {
        this.documentos.set([...this.documentos(), response]);
        this.archivoSeleccionado.set(null);
        this.mostrarFormulario.set(false);
        this.cargando.set(false);
      },
      error: () => this.cargando.set(false)
    });
  }

  eliminarDocumento(documentoId: number): void {
    this.cargando.set(true);
    this.documentosService.eliminar(documentoId, this.usuarioId).subscribe({
      next: () => {
        this.documentos.set(
          this.documentos().filter((d: DocumentoPadre) => d.id !== documentoId)
        );
        this.cargando.set(false);
      },
      error: () => this.cargando.set(false)
    });
  }

  descargarDocumento(documentoId: number): void {
    this.documentosService.descargar(documentoId).subscribe({
      next: (blob: Blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'documento';
        a.click();
        window.URL.revokeObjectURL(url);
      }
    });
  }

  marcarVisto(documentoId: number): void {
    this.documentosService.marcarVisto(documentoId, this.usuarioId).subscribe({
      next: () => {
        this.documentos.set(
          this.documentos().map((d: DocumentoPadre) =>
            d.id === documentoId ? { ...d, visto: true } : d
          )
        );
      }
    });
  }
}

