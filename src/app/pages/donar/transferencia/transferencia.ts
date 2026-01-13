import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-transferencia',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './transferencia.html',
  styleUrls: ['./transferencia.scss']
})
export class TransferenciaComponent {
  monto: number | null = null;
  comprobante: File | null = null;

  subirComprobante(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.comprobante = file;
      alert(`Comprobante recibido: ${file.name}`);
    }
  }

  confirmarTransferencia() {
    if (!this.monto || !this.comprobante) {
      alert('Por favor indica el monto y sube tu comprobante.');
      return;
    }
    alert(`Gracias por tu donación de $${this.monto} MXN. Comprobante: ${this.comprobante.name}. ¡Tu apoyo marca la diferencia!`);
  }
}



