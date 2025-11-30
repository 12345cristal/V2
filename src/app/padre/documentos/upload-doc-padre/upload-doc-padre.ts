import { Component, Input, signal } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';
import { DocumentosService } from '../../../service/documentos.service';

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

  form = this.fb.group({
    titulo: ['', [Validators.required, Validators.minLength(5)]],
    descripcion: [''],
    tipo: ['RECETA_MEDICA', Validators.required],
    parentesco: ['MAMA', Validators.required],
    visibleParaTerapeutas: [true],
  });

  constructor(private fb: FormBuilder, private docs: DocumentosService) {}

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

    const dto = {
      ...this.form.value,
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
