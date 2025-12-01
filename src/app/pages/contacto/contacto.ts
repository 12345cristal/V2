import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HeaderComponent } from '../../shared/header/header';
import { FooterComponent } from '../../shared/footer/footer';

@Component({
  selector: 'app-contacto',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HeaderComponent, FooterComponent],
  templateUrl: './contacto.html',
  styleUrls: ['./contacto.scss']
})
export class Contacto {
  contactoForm: FormGroup;
  enviando = false;
  mensajeExito = '';
  mensajeError = '';

  constructor(private fb: FormBuilder) {
    this.contactoForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.pattern(/^[a-zA-Z\s]+$/)]],
      correo: ['', [Validators.required, Validators.email]],
      telefono: ['', [Validators.required, Validators.pattern(/^\+?\d{10,15}$/)]],
      mensaje: ['', [Validators.required, Validators.minLength(10)]]
    });
  }

  campoInvalido(campo: string): boolean {
    const control = this.contactoForm.get(campo);
    return !!(control && control.invalid && (control.dirty || control.touched));
  }

  enviar() {
    if (this.contactoForm.invalid) {
      this.contactoForm.markAllAsTouched();
      return;
    }

    this.enviando = true;
    // Simulación de envío
    setTimeout(() => {
      this.mensajeExito = 'Mensaje enviado con éxito. ¡Gracias por contactarnos!';
      this.mensajeError = '';
      this.enviando = false;
      this.contactoForm.reset();
    }, 1500);
  }
}
