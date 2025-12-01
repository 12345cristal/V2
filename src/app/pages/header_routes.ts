import { Routes } from '@angular/router';

// Importaciones de las páginas principales
import { ServiciosComponent } from '../pages/servicios/servicios';
import { Contacto } from '../pages/contacto/contacto';
import { Equipo } from '../pages/equipo/equipo';
import { Ventas } from '../pages/ventas/ventas';
import { DonarComponent } from '../pages/donar/donar';
import { Login } from '../pages/login/login';

// Importaciones de los subcomponentes de Donar
import { TransferenciaComponent } from '../pages/donar/transferencia/transferencia';
import { Paypal } from '../pages/donar/paypal/paypal';
import { DepositoComponent } from '../pages/donar/deposito/deposito';

export const HEADER_ROUTES: Routes = [
  { path: 'servicios', component: ServiciosComponent },
  { path: 'contacto', component: Contacto },
  { path: 'equipo', component: Equipo },
  { path: 'ventas', component: Ventas },

  // Ruta padre Donar
  { 
    path: 'donar', 
    component: DonarComponent,
    children: [
      { path: 'deposito', component: DepositoComponent },
      { path: 'transferencia', component: TransferenciaComponent },
      { path: 'paypal', component: Paypal }    ]
  },

  { path: 'login', component: Login },

  // Ruta por defecto
  { path: '', redirectTo: 'servicios', pathMatch: 'full' },
];
