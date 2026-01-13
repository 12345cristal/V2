import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HeaderComponent } from '../../shared/header/header';
import { FooterComponent } from '../../shared/footer/footer';
import { ChatbotIaComponent } from '../../shared/chatbot-ia/chatbot-ia.component';


@Component({
  selector: 'app-contact',
  standalone: true,  
  imports: [
    CommonModule, 
    ReactiveFormsModule,
    HeaderComponent,     
    FooterComponent,
    ChatbotIaComponent     
  ],
  templateUrl: './contacto.html',
  styleUrls: ['./contacto.scss']
})

export class ContactComponent implements OnInit {
  contactForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.contactForm = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(2)]], // Agregué minLength
      apellido: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      telefono: [''], // Opcional
      asunto: ['', Validators.required],
      mensaje: ['', [Validators.required, Validators.minLength(10)]] // Mínimo 10 caracteres
    });
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    if (this.contactForm.valid) {
      console.log('Formulario enviado:', this.contactForm.value);
      alert('Mensaje enviado correctamente');
      this.contactForm.reset();
    } else {
      this.contactForm.markAllAsTouched();
    }
  }

  campoNoValido(campo: string): boolean {
    const control = this.contactForm.get(campo);
    return control ? (control.invalid && control.touched) : false;
  }

}



