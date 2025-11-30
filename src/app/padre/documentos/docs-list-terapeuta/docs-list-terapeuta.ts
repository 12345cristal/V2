import { Component, Input, OnInit, signal } from '@angular/core';
import { DocumentosService } from '../../services/documentos.service';

@Component({
  selector: 'app-docs-list-terapeuta',
  standalone: true,
  templateUrl: './docs-list-terapeuta.html',
  styleUrls: ['./docs-list-terapeuta.scss']
})
export default class DocsListTerapeutaComponent implements OnInit {

  @Input() ninoId!: number;

  documentos = signal([]);

  constructor(private docs: DocumentosService) {}

  ngOnInit(): void {
    this.docs.getTerapeutaDocs(this.ninoId)
      .subscribe(r => this.documentos.set(r));
  }

  descargar(doc: any) {
    window.open(doc.urlArchivo, '_blank');
  }
}
