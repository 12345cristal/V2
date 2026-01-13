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

  @Output() abrir = new EventEmitter<void>();
  @Output() descargar = new EventEmitter<void>();
}




