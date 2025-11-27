import { Routes } from '@angular/router';

/* ==== IMPORTS DEL MÓDULO COORDINADOR ==== */
import { CitasComponent } from './citas/citas';
import { Ninos } from './ninos/ninos/ninos';
import { NinoForm } from './ninos/nino-form/nino-form';
import { UsuariosComponent } from './usuarios/usuarios';
import { UsuarioFormComponent } from './usuarios/usuarios-form/usuarios-form';
import { TerapiasComponent } from './terapias/terapias';
import { PerfilComponent } from './perfil/perfil';
import { Layout } from './layout/layout';

/* ==== IMPORTS DEL MÓDULO PERSONAL ==== */
import { PersonalListComponent } from './personal/personal-list/personal-list';
import { PersonalFormComponent } from './personal/personal-form/personal-form';
import { PersonalDetalleComponent } from './personal/personal-detalle/personal-detalle';
import { PersonalHorariosComponent } from './personal/personal-horarios/personal-horarios';


export const COORDINADOR_ROUTES: Routes = [
  {
    path: '',
    component: Layout,
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
      { path: 'nino/:id', component: NinoForm },
      { path: 'nino/:id/editar', component: NinoForm },

      /* =======================================
         🟦 MÓDULO USUARIOS
      ======================================= */
      { path: 'usuarios', component: UsuariosComponent },                // LISTA
      { path: 'usuarios/nuevo', component: UsuarioFormComponent },      // NUEVO USUARIO
      { path: 'usuarios/editar/:id', component: UsuarioFormComponent }, // EDITAR USUARIO

      /* =======================================
         🔵 OTRAS RUTAS
      ======================================= */
      { path: 'citas', component: CitasComponent },
      { path: 'terapias', component: TerapiasComponent },

      /* =======================================
         🟩 PERFIL (YA AGREGADO)
      ======================================= */
      { path: 'perfil', component: PerfilComponent },

     
      /* DEFAULT */
      { path: '', redirectTo: 'citas', pathMatch: 'full' },
    ],
  },
];
