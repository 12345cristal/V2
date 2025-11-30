import { Component, Input, OnInit, signal } from '@angular/core';
import { DocumentosService } from '../../../service/documentos.service';

@Component({
  selector: 'app-docs-list-padre',
  standalone: true,
  templateUrl: './docs-list-padre.html',
  styleUrls: ['./docs-list-padre.scss']
})
export default class DocsListPadreComponent implements OnInit {

  @Input() ninoId!: number;

  documentos = signal([]);

  constructor(private docs: DocumentosService) {}

  ngOnInit(): void {
    this.load();
  }

  load() {
    this.docs.getPadreDocs(this.ninoId).subscribe(r => this.documentos.set(r));
  }

  eliminar(doc: any) {
    this.docs.eliminar(doc.id).subscribe(() => {
      this.load();
    });
  }

  descargar(doc: any) {
    window.open(doc.urlArchivo, '_blank');
  }
}
