import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardComponent } from '../shared/card/card.component';
import { TablaComponent, TableColumn } from '../shared/tabla/tabla.component';

interface Pago {
  id: string;
  fecha: Date;
  concepto: string;
  monto: number;
  metodoPago: string;
  estado: 'pagado' | 'pendiente' | 'vencido';
  factura?: string;
}

interface Plan {
  nombre: string;
  montoPlan: number;
  montoPagado: number;
  saldoPendiente: number;
  proximaFecha: Date;
}

@Component({
  selector: 'app-pagos',
  standalone: true,
  imports: [CommonModule, CardComponent, TablaComponent],
  templateUrl: './pagos.component.html',
  styleUrls: ['./pagos.component.scss'],
})
export class PagosComponent implements OnInit {
  plan?: Plan;
  pagos: Pago[] = [];
  columns: TableColumn[] = [];
  
  ngOnInit() {
    this.cargarPlan();
    this.cargarPagos();
    this.setupColumns();
  }
  
  private cargarPlan() {
    this.plan = {
      nombre: 'Plan Mensual - Terapia Integral',
      montoPlan: 1500000,
      montoPagado: 1000000,
      saldoPendiente: 500000,
      proximaFecha: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
    };
  }
  
  private cargarPagos() {
    this.pagos = [
      {
        id: '1',
        fecha: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
        concepto: 'Terapia Mensual - Enero',
        monto: 500000,
        metodoPago: 'Tarjeta de Crédito',
        estado: 'pagado',
        factura: 'FACT-2024-001'
      },
      {
        id: '2',
        fecha: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000),
        concepto: 'Terapia Mensual - Diciembre',
        monto: 500000,
        metodoPago: 'Transferencia Bancaria',
        estado: 'pagado',
        factura: 'FACT-2023-012'
      },
      {
        id: '3',
        fecha: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
        concepto: 'Terapia Mensual - Febrero',
        monto: 500000,
        metodoPago: 'Pendiente',
        estado: 'pendiente'
      }
    ];
  }
  
  private setupColumns() {
    this.columns = [
      { key: 'fecha', label: 'Fecha', sortable: true },
      { key: 'concepto', label: 'Concepto', sortable: false },
      { key: 'monto', label: 'Monto', sortable: true },
      { key: 'metodoPago', label: 'Método de Pago', sortable: false },
      { key: 'estado', label: 'Estado', sortable: true }
    ];
  }
  
  get porcentajePagado(): number {
    if (!this.plan) return 0;
    return (this.plan.montoPagado / this.plan.montoPlan) * 100;
  }
  
  descargarFactura(pago: Pago) {
    console.log('Descargando factura:', pago.factura);
    // Implementar descarga de factura
  }
  
  realizarPago() {
    console.log('Redirigir a pasarela de pago');
    // Implementar redirección a pasarela de pago
  }
}
