import { Routes } from '@angular/router';

/* =======================================
   📌 IMPORTS — MÓDULO COORDINADOR
======================================= */
import { CitasComponent } from './citas/citas';
import { Ninos } from './ninos/ninos/ninos';
import { NinoForm } from './ninos/nino-form/nino-form';
import { PerfilNinoComponent } from './perfil-nino/perfil-nino.component';
import { UsuariosComponent } from './usuarios/usuarios';
import { UsuarioFormComponent } from './usuarios/usuarios-form/usuarios-form';
import { TerapiasComponent } from './terapias/terapias';
import { TerapiasNuevoComponent } from './terapias/terapias-nuevo';
import { PrioridadNinosComponent } from './prioridad-nino/prioridad-ninos';
import { InicioComponent } from './inicio/inicio';
import { AsignarTerapiasComponent } from './asignar-terapias/asignar-terapias.component';

/* =======================================
   📌 IMPORTS — MÓDULO TOPSIS Y RECOMENDACIÓN
======================================= */
import { PrioridadNinosComponent as TopsisPrioridadComponent } from './prioridad-ninos/prioridad-ninos';
import { RecomendacionNinoComponent } from './recomendacion-nino/recomendacion-nino';
import { TopsisTerapeutasComponent } from './topsis-terapeutas/topsis-terapeutas';
import { RecomendacionesActividadesComponent } from './recomendaciones-actividades/recomendaciones-actividades';

/* =======================================
   📌 IMPORTS — MÓDULO PERSONAL
======================================= */
import { PersonalListComponent } from './personal/personal-list/personal-list';
import { PersonalFormComponent } from './personal/personal-form/personal-form';
import { PersonalDetalleComponent } from './personal/personal-detalle/personal-detalle';
import { PersonalHorariosComponent } from './personal/personal-horarios/personal-horarios';

/* =======================================
   📌 IMPORTS — FICHAS DE EMERGENCIA
======================================= */
import { FichasEmergenciaComponent } from './fichas-emergencia/fichas-emergencia.component';

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
      // Ruta de horarios eliminada según requerimiento

      /* =======================================
         🟣 MÓDULO NIÑOS
      ======================================= */
      { path: 'ninos', component: Ninos },
      { path: 'nino/nuevo', component: NinoForm },
      { path: 'nino/:id/editar', component: NinoForm },
      { path: 'nino/:id/perfil', component: PerfilNinoComponent },

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
      { path: 'terapias-nuevo', component: TerapiasNuevoComponent },
      { path: 'asignar-terapias', component: AsignarTerapiasComponent },

      /* =======================================
         🟨 MÓDULO CITAS
      ======================================= */
      { path: 'citas', component: CitasComponent },

      /* =======================================
         🟩 MÓDULO DECISION SUPPORT (TOPSIS)
      ======================================= */
      { path: 'prioridad-ninos', component: PrioridadNinosComponent },
      { path: 'topsis-prioridad', component: TopsisPrioridadComponent },

      /* =======================================
         🟪 MÓDULO RECOMENDACIÓN
      ======================================= */
      { path: 'recomendacion-nino', component: RecomendacionNinoComponent },

      /* =======================================
         🟧 MÓDULO TOPSIS TERAPEUTAS
      ======================================= */
      { path: 'topsis-terapeutas', component: TopsisTerapeutasComponent },

      /* =======================================
         🎯 MÓDULO RECOMENDACIONES DE ACTIVIDADES
      ======================================= */
      { path: 'recomendaciones-actividades', component: RecomendacionesActividadesComponent },

      /* =======================================
         🚨 MÓDULO FICHAS DE EMERGENCIA
      ======================================= */
      { path: 'fichas-emergencia', component: FichasEmergenciaComponent },
{
    path: 'mensajes',
    loadComponent: () =>
      import('../shared/mensajes/mensajes.component')
        .then(c => c.MensajesComponent),
  },
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

