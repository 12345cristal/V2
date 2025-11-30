import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import DocsListPadreComponent from '../../../components/docs-list-padre/docs-list-padre';
import DocsListTerapeutaComponent from '../../../components/docs-list-terapeuta/docs-list-terapeuta';
import UploadDocPadreComponent from '../../../components/upload-doc-padre/upload-doc-padre';

@Component({
  selector: 'app-documentos-padre',
  standalone: true,
  imports: [
    DocsListPadreComponent,
    DocsListTerapeutaComponent,
    UploadDocPadreComponent
  ],
  templateUrl: './documentos-padre.component.html',
  styleUrls: ['./documentos-padre.component.scss']
})
export default class DocumentosPadreComponent implements OnInit {

  ninoId!: number;

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.ninoId = Number(this.route.snapshot.paramMap.get('id'));
  }
}
