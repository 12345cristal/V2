import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

// Services
import { PadreService } from './services/padre.service';
import { SesionesService } from './services/sesiones.service';
import { PagosService } from './services/pagos.service';
import { DocumentosPadreService } from './services/documentos.service';
import { MensajesService } from './services/mensajes.service';
import { RecursosService } from './services/recursos.service';
import { TareasService } from './services/tareas.service';

/**
 * Módulo principal del Padre
 * Agrupa todos los servicios y configuraciones del módulo padre
 */
@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [
    PadreService,
    SesionesService,
    PagosService,
    DocumentosPadreService,
    MensajesService,
    RecursosService,
    TareasService
  ]
})
export class PadreModule { }
