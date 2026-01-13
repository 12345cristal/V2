import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-pdf-viewer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './pdf-viewer.component.html',
  styleUrls: ['./pdf-viewer.component.scss'],
})
export class PdfViewerComponent {
  @Input() title = 'Documento PDF';
  @Input() safeUrl: SafeResourceUrl | null = null;
  @Input() filename = 'archivo.pdf';
  @Input() pdfSrc: string = '';

  @Output() abrir = new EventEmitter<void>();
  @Output() descargar = new EventEmitter<void>();

  rawUrl: string = ''; // Agregar esta propiedad

  // Si rawUrl debe ser calculada a partir de pdfSrc:
  ngOnChanges() {
    if (this.pdfSrc) {
      this.rawUrl = this.pdfSrc; // O la lógica que necesites
    }
  }
}
