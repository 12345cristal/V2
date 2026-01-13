import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import DocsListPadreComponent from './docs-list-padre/docs-list-padre';
import DocsListTerapeutaComponent from './docs-list-terapeuta/docs-list-terapeuta';
import UploadDocPadreComponent from './upload-doc-padre/upload-doc-padre';

@Component({
  selector: 'app-documentos-padre',
  standalone: true,
  imports: [
    DocsListPadreComponent,
    DocsListTerapeutaComponent,
    UploadDocPadreComponent
  ],
  templateUrl: './documentos.html',
  styleUrls: ['./documentos.scss']
})
export default class DocumentosPadreComponent implements OnInit {

  ninoId!: number;

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.ninoId = Number(this.route.snapshot.paramMap.get('id'));
  }
}

