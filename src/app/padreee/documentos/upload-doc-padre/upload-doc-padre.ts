import { Component, Input, signal } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule, FormGroup } from '@angular/forms';
import { DocumentosService } from '../../../service/documentos.service';
import { CrearDocumentoPadreDto, TipoDocumento } from '../../../interfaces/documento.interface';

@Component({
  selector: 'app-upload-doc-padre',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './upload-doc-padre.html',
  styleUrls: ['./upload-doc-padre.scss']
})
export default class UploadDocPadreComponent {

  @Input() ninoId!: number;

  archivo = signal<File | null>(null);
  advertencia = signal<string | null>(null);
  enviado = signal(false);

  // ✔ Declaramos la propiedad SIN inicializar
  form!: FormGroup;

  constructor(private fb: FormBuilder, private docs: DocumentosService) {

    // ✔ Se inicializa aquí, cuando fb YA existe
    this.form = this.fb.group({
      titulo: ['', [Validators.required, Validators.minLength(5)]],
      descripcion: [''],
      tipo: ['RECETA_MEDICA' as TipoDocumento, Validators.required],
      parentesco: ['MAMA', Validators.required],
      visibleParaTerapeutas: [true],
    });
  }

  onFile(event: any) {
    const file = event.target.files[0];
    if (!file) {
      this.archivo.set(null);
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      this.advertencia.set('El archivo supera los 10 MB');
      return;
    }

    this.archivo.set(file);
  }

  enviar() {
    this.advertencia.set(null);
    this.enviado.set(true);

    if (this.form.invalid) {
      this.advertencia.set('Faltan datos obligatorios.');
      return;
    }

    if (!this.archivo()) {
      this.advertencia.set('Debes seleccionar un archivo.');
      return;
    }

    const dto: CrearDocumentoPadreDto = {
      titulo: this.form.get('titulo')!.value as string,
      descripcion: this.form.get('descripcion')!.value ?? '',
      tipo: this.form.get('tipo')!.value as TipoDocumento,  // ✔ corregido
      parentesco: this.form.get('parentesco')!.value as string,
      visibleParaTerapeutas: this.form.get('visibleParaTerapeutas')!.value as boolean,
      ninoId: this.ninoId,
      archivo: this.archivo()!
    };

    this.docs.subirDocumento(dto).subscribe(() => {
      this.form.reset({
        tipo: 'RECETA_MEDICA',
        parentesco: 'MAMA',
        visibleParaTerapeutas: true
      });
      this.archivo.set(null);
      this.enviado.set(false);
    });
  }
}

