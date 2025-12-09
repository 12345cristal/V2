import { Routes } from '@angular/router';

/* =======================================
   📌 IMPORTS — MÓDULO COORDINADOR
======================================= */
import { CitasComponent } from './citas/citas';
import { Ninos } from './ninos/ninos/ninos';
import { NinoForm } from './ninos/nino-form/nino-form';
import { UsuariosComponent } from './usuarios/usuarios';
import { UsuarioFormComponent } from './usuarios/usuarios-form/usuarios-form';
import { TerapiasComponent } from './terapias/terapias';
import { PrioridadNinosComponent } from './prioridad-nino/prioridad-ninos';
import { InicioComponent } from './inicio/inicio';

/* =======================================
   📌 IMPORTS — MÓDULO PERSONAL
======================================= */
import { PersonalListComponent } from './personal/personal-list/personal-list';
import { PersonalFormComponent } from './personal/personal-form/personal-form';
import { PersonalDetalleComponent } from './personal/personal-detalle/personal-detalle';
import { PersonalHorariosComponent } from './personal/personal-horarios/personal-horarios';

/* =======================================
   📌 IMPORTS — SHARED / LAYOUT
======================================= */
import { PerfilComponent } from '../shared/perfil/perfil';
import { LayoutComponent } from '../shared/layout/layout';
import { AuthGuard } from '../guards/auth.guard';
import { RoleGuard } from '../guards/role.guard';

export const COORDINADOR_ROUTES: Routes = [
  {
    path: '',
    component: LayoutComponent,
    children: [

      /* =======================================
         🔵 MÓDULO PERSONAL
      ======================================= */
      { path: 'personal', component: PersonalListComponent },
      { path: 'personal/nuevo', component: PersonalFormComponent },
      { path: 'personal/editar/:id', component: PersonalFormComponent },
      { path: 'personal/detalle/:id', component: PersonalDetalleComponent },
      { path: 'personal/horarios/:id', component: PersonalHorariosComponent },

      /* =======================================
         🟣 MÓDULO NIÑOS
      ======================================= */
      { path: 'ninos', component: Ninos },
      { path: 'nino/nuevo', component: NinoForm },
      { path: 'nino/:id/editar', component: NinoForm },

      /* =======================================
         🟦 MÓDULO USUARIOS
      ======================================= */
      { path: 'usuarios', component: UsuariosComponent },
      { path: 'usuarios/nuevo', component: UsuarioFormComponent },
      { path: 'usuarios/editar/:id', component: UsuarioFormComponent },

      /* =======================================
         🟧 MÓDULO TERAPIAS
      ======================================= */
      { path: 'terapias', component: TerapiasComponent },

      /* =======================================
         🟨 MÓDULO CITAS
      ======================================= */
      { path: 'citas', component: CitasComponent },

      /* =======================================
         🟩 MÓDULO DECISION SUPPORT (TOPSIS)
      ======================================= */
      { path: 'prioridad-ninos', component: PrioridadNinosComponent },

      /* =======================================
         🟩 PERFIL
      ======================================= */
      { path: 'perfil', component: PerfilComponent },

      /* =======================================
         🔵 DETALLE TERAPEUTA (Lazy Load + Guards)
      ======================================= */
      {
        path: 'terapeutas/:id',
        canActivate: [AuthGuard, RoleGuard],
        data: { roles: [1, 2] }, // admin, coordinador
        loadComponent: () =>
          import('./terapeuta-detalle/terapeuta-detalle')
            .then(m => m.TerapeutaDetalleComponent)
      },

      {
        path: 'auditoria',
        canActivate: [AuthGuard, RoleGuard],
        data: { roles: [1, 2] },
        loadComponent: () =>
          import('./auditoria/auditoria')
            .then(m => m.AuditoriaComponent),
      },

      /* =======================================
         🏠 DASHBOARD/INICIO
      ======================================= */
      { path: 'inicio', component: InicioComponent },

      /* =======================================
         🔻 DEFAULT REDIRECT
      ======================================= */
      { path: '', redirectTo: 'inicio', pathMatch: 'full' },
    ],
  },
];
