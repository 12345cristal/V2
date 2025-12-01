import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../../shared/header/header';
import { FooterComponent } from '../../shared/footer/footer';

interface Producto {
  nombre: string;
  descripcion: string;
  precio: number;
  imagen: string;
}

@Component({
  selector: 'app-ventas',
  standalone: true,
  imports: [CommonModule, HeaderComponent, FooterComponent],
  templateUrl: './ventas.html',
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
