import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-paypal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './paypal.html',
  styleUrls: ['./paypal.scss']
})
export class Paypal {
  montoPaypal: number | null = null;

  donarPayPal() {
    if (!this.montoPaypal || this.montoPaypal <= 0) {
      alert('Por favor ingresa un monto válido.');
      return;
    }
    // Abre la página oficial de PayPal para la donación
    const url = `https://www.paypal.me/AutismoMochis/${this.montoPaypal}`;
    window.open(url, '_blank');
  }
}



