import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../../shared/header/header';
import { FooterComponent } from '../../shared/footer/footer';
import { ChatbotIaComponent } from '../../shared/chatbot-ia/chatbot-ia.component';

interface Producto {
  nombre: string;
  descripcion: string;
  precio: number;
  imagen: string;
}

@Component({
  selector: 'app-ventas',
  standalone: true,
  imports: [CommonModule, HeaderComponent, FooterComponent, ChatbotIaComponent],
  template: `
    <app-header></app-header>

    <section class="ventas-container">
      <div class="section-header">
        <h1>Tienda Autismo Mochis</h1>
        <h2>Apoya nuestra causa adquiriendo productos oficiales</h2>
      </div>

      <div class="productos-grid">
        <div class="producto-card" *ngFor="let producto of productos">
          <img [src]="producto.imagen" [alt]="producto.nombre" class="producto-img"/>
          <h3>{{ producto.nombre }}</h3>
          <p>$ {{ producto.precio }} MXN</p>
          <button class="info-button" (click)="comprar(producto)">
            Ver detalles / Comprar
          </button>
        </div>
      </div>
    </section>

    <app-chatbot-ia></app-chatbot-ia>
    <app-footer></app-footer>
  `,
  styleUrls: ['./ventas.scss']
})
export class Ventas {
  productos: Producto[] = [
    {
      nombre: 'Playera Autismo Mochis',
      descripcion: 'Playera con diseño oficial de Autismo Mochis, cómoda y de buena calidad.',
      precio: 250,
      imagen: 'ventas/playera.jpg'
    },
    {
      nombre: 'Café Autismo Mochis',
      descripcion: 'Café artesanal de Autismo Mochis, sabor delicioso y 100% orgánico.',
      precio: 250,
      imagen: 'ventas/cafe.jpg'
    },
    {
      nombre: 'Taza Autismo Mochis',
      descripcion: 'Taza con el logo de Autismo Mochis, perfecta para tu bebida favorita.',
      precio: 300,
      imagen: 'ventas/taza.jpg'
    }
  ];

  // Función para abrir WhatsApp con mensaje
  comprar(producto: Producto) {
    const numero = '6681484934'; // 52 + lada México + número
    const mensaje = `Hola, quiero comprar el producto: ${producto.nombre} por $${producto.precio} MXN`;
    window.open(`https://wa.me/${numero}?text=${encodeURIComponent(mensaje)}`, '_blank');
  }
}

