import { Routes } from '@angular/router';

// Importaciones de las páginas principales
import { ServiciosComponent } from '../pages/servicios/servicios';
import { ContactComponent } from '../pages/contacto/contacto';
import { Equipo } from '../pages/equipo/equipo';
import { Ventas } from '../pages/ventas/ventas';
import { DonarComponent } from '../pages/donar/donar';
import { LoginComponent } from '../pages/login/login';

// Subrutas de Donar
import { DepositoComponent } from '../pages/donar/deposito/deposito';
import { TransferenciaComponent } from '../pages/donar/transferencia/transferencia';
import { Paypal } from '../pages/donar/paypal/paypal';

export const HEADER_ROUTES: Routes = [
  { path: 'servicios', component: ServiciosComponent },
  { path: 'contacto', component: ContactComponent },
  { path: 'equipo', component: Equipo },
  { path: 'ventas', component: Ventas },

  {
    path: 'donar',
    component: DonarComponent,
    children: [
      { path: 'deposito', component: DepositoComponent },
      { path: 'transferencia', component: TransferenciaComponent },
      { path: 'paypal', component: Paypal },
    ]
  },

  { path: 'login', component: LoginComponent },
];
