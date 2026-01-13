import { Component, Input, OnInit, signal } from '@angular/core';
import { DocumentosService } from '../../../service/documentos.service';
import { DocumentoPadre } from '../../../interfaces/documento.interface';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-docs-list-padre',
  standalone: true,
  imports: [
    DatePipe // Necesario para | date
  ],
  templateUrl: './docs-list-padre.html',
  styleUrls: ['./docs-list-padre.scss']
})
export default class DocsListPadreComponent implements OnInit {

  @Input() ninoId!: number;

  // ⬅ MUY IMPORTANTE: TIPAR EL SIGNAL
  documentos = signal<DocumentoPadre[]>([]);

  constructor(private docs: DocumentosService) {}

  ngOnInit(): void {
    this.load();
  }

  load() {
    this.docs.getPadreDocs(this.ninoId).subscribe(resp => {
      this.documentos.set(resp);
    });
  }

  eliminar(doc: DocumentoPadre) {
    this.docs.eliminar(doc.id).subscribe(() => {
      this.load();
    });
  }

  descargar(doc: DocumentoPadre) {
    window.open(doc.urlArchivo, '_blank');
  }
}

