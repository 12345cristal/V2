import { Component, Input, OnInit, signal } from '@angular/core';
import { DocumentosService } from '../../../service/documentos.service';
import { DocumentoTerapeuta } from '../../../interfaces/documento.interface';
import { DatePipe, NgFor, NgIf } from '@angular/common'; // ⬅ IMPORTANTE

@Component({
  selector: 'app-docs-list-terapeuta',
  standalone: true,
  imports: [
    DatePipe,   // ⬅ Necesario para usar |date
  ],
  templateUrl: './docs-list-terapeuta.html',
  styleUrls: ['./docs-list-terapeuta.scss']
})
export default class DocsListTerapeutaComponent implements OnInit {

  @Input() ninoId!: number;

  documentos = signal<DocumentoTerapeuta[]>([]);

  constructor(private docs: DocumentosService) {}

  ngOnInit(): void {
    this.docs.getTerapeutaDocs(this.ninoId)
      .subscribe(resp => this.documentos.set(resp));
  }

  descargar(doc: DocumentoTerapeuta) {
    window.open(doc.urlArchivo, '_blank');
  }
}
