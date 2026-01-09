import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { TerapeutaService } from '../../service/terapeuta.service';

interface Conversacion {
  id_conversacion: number;
  tipo_participante: 'padre' | 'terapeuta' | 'coordinador';
  nombre_participante: string;
  avatar?: string;
  ultimo_mensaje: string;
  fecha_ultimo: Date;
  no_leidos: number;
}

interface Mensaje {
  id_mensaje: number;
  emisor: string;
  es_propio: boolean;
  mensaje: string;
  fecha: Date;
  leido: boolean;
}

@Component({
  selector: 'app-mensajes-terapeuta',
  standalone: true,
  imports: [CommonModule, FormsModule, MatIconModule],
  template: `
    <div class="mensajes-container">
      <!-- Sidebar de conversaciones -->
      <aside class="conversaciones-sidebar">
        <div class="sidebar-header">
          <h2>Mensajes</h2>
          <button class="btn-nuevo-mensaje" (click)="nuevoMensaje()">
            <mat-icon>add</mat-icon>
          </button>
        </div>

        <div class="busqueda">
          <mat-icon>search</mat-icon>
          <input 
            type="text" 
            [(ngModel)]="busquedaConversacion"
            (input)="filtrarConversaciones()"
            placeholder="Buscar conversación..."
          />
        </div>

        <div class="lista-conversaciones">
          @for (conv of conversacionesFiltradas(); track conv.id_conversacion) {
            <article 
              class="conversacion-item"
              [class.activa]="conv.id_conversacion === conversacionActiva()?.id_conversacion"
              [class.no-leida]="conv.no_leidos > 0"
              (click)="seleccionarConversacion(conv)"
            >
              <div class="avatar">
                @if (conv.avatar) {
                  <img [src]="conv.avatar" [alt]="conv.nombre_participante" />
                } @else {
                  <mat-icon>{{ getIconoTipo(conv.tipo_participante) }}</mat-icon>
                }
              </div>

              <div class="conv-info">
                <div class="conv-header">
                  <h4>{{ conv.nombre_participante }}</h4>
                  <span class="tiempo">{{ conv.fecha_ultimo | date: 'HH:mm' }}</span>
                </div>
                <p class="ultimo-mensaje">{{ conv.ultimo_mensaje }}</p>
              </div>

              @if (conv.no_leidos > 0) {
                <span class="badge-no-leidos">{{ conv.no_leidos }}</span>
              }
            </article>
          }
        </div>
      </aside>

      <!-- Chat principal -->
      <main class="chat-principal">
        @if (conversacionActiva()) {
          @let conv = conversacionActiva()!;

          <!-- Header del chat -->
          <header class="chat-header">
            <button class="btn-volver-mobile" (click)="cerrarChat()">
              <mat-icon>arrow_back</mat-icon>
            </button>

            <div class="participante-info">
              <div class="avatar-small">
                @if (conv.avatar) {
                  <img [src]="conv.avatar" [alt]="conv.nombre_participante" />
                } @else {
                  <mat-icon>{{ getIconoTipo(conv.tipo_participante) }}</mat-icon>
                }
              </div>
              <div>
                <h3>{{ conv.nombre_participante }}</h3>
                <p class="tipo-usuario">{{ getTipoTexto(conv.tipo_participante) }}</p>
              </div>
            </div>

            <button class="btn-opciones">
              <mat-icon>more_vert</mat-icon>
            </button>
          </header>

          <!-- Área de mensajes -->
          <div class="mensajes-area" #mensajesContainer>
            @for (mensaje of mensajes(); track mensaje.id_mensaje) {
              <div class="mensaje" [class.propio]="mensaje.es_propio">
                <div class="mensaje-burbuja">
                  <p>{{ mensaje.mensaje }}</p>
                  <span class="hora">{{ mensaje.fecha | date: 'HH:mm' }}</span>
                </div>
              </div>
            }
          </div>

          <!-- Input de mensaje -->
          <div class="mensaje-input">
            <button class="btn-adjuntar">
              <mat-icon>attach_file</mat-icon>
            </button>
            <input 
              type="text"
              [(ngModel)]="nuevoMensajeTexto"
              (keyup.enter)="enviarMensaje()"
              placeholder="Escribe un mensaje..."
            />
            <button 
              class="btn-enviar"
              [disabled]="!nuevoMensajeTexto.trim()"
              (click)="enviarMensaje()"
            >
              <mat-icon>send</mat-icon>
            </button>
          </div>

        } @else {
          <!-- Estado vacío -->
          <div class="chat-vacio">
            <mat-icon>chat</mat-icon>
            <h3>Selecciona una conversación</h3>
            <p>Elige una conversación de la lista para comenzar</p>
          </div>
        }
      </main>
    </div>
  `,
  styles: [`
    .mensajes-container {
      display: grid;
      grid-template-columns: 350px 1fr;
      height: calc(100vh - 80px);
      background: #f9fafb;
      overflow: hidden;
    }

    /* ===== SIDEBAR ===== */
    .conversaciones-sidebar {
      background: white;
      border-right: 1px solid #e5e7eb;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    .sidebar-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px;
      border-bottom: 1px solid #e5e7eb;
    }

    .sidebar-header h2 {
      font-size: 1.5rem;
      font-weight: 700;
      color: #1f2937;
      margin: 0;
    }

    .btn-nuevo-mensaje {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border: none;
      background: #4a90e2;
      color: white;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;
    }

    .btn-nuevo-mensaje:hover {
      background: #357abd;
      transform: scale(1.1);
    }

    .busqueda {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 20px;
      background: #f9fafb;
      border-bottom: 1px solid #e5e7eb;
    }

    .busqueda mat-icon {
      color: #6b7280;
      font-size: 20px;
    }

    .busqueda input {
      flex: 1;
      border: none;
      background: transparent;
      outline: none;
      font-size: 0.9rem;
    }

    .lista-conversaciones {
      flex: 1;
      overflow-y: auto;
    }

    .conversacion-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px 20px;
      cursor: pointer;
      transition: background 0.3s ease;
      border-bottom: 1px solid #f3f4f6;
      position: relative;
    }

    .conversacion-item:hover {
      background: #f9fafb;
    }

    .conversacion-item.activa {
      background: #e3f2fd;
      border-left: 4px solid #4a90e2;
    }

    .conversacion-item.no-leida {
      background: #fffbeb;
    }

    .avatar {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: #e5e7eb;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .avatar img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 50%;
    }

    .avatar mat-icon {
      color: #6b7280;
      font-size: 28px;
    }

    .conv-info {
      flex: 1;
      min-width: 0;
    }

    .conv-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
    }

    .conv-header h4 {
      font-size: 0.95rem;
      font-weight: 600;
      color: #1f2937;
      margin: 0;
    }

    .tiempo {
      font-size: 0.75rem;
      color: #6b7280;
    }

    .ultimo-mensaje {
      font-size: 0.875rem;
      color: #6b7280;
      margin: 0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .badge-no-leidos {
      min-width: 20px;
      height: 20px;
      border-radius: 10px;
      background: #4a90e2;
      color: white;
      font-size: 0.75rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 6px;
    }

    /* ===== CHAT PRINCIPAL ===== */
    .chat-principal {
      display: flex;
      flex-direction: column;
      background: white;
      overflow: hidden;
    }

    .chat-header {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px 20px;
      border-bottom: 1px solid #e5e7eb;
      background: white;
    }

    .btn-volver-mobile {
      display: none;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      border: none;
      background: #e5e7eb;
      cursor: pointer;
    }

    .participante-info {
      display: flex;
      align-items: center;
      gap: 12px;
      flex: 1;
    }

    .avatar-small {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: #e5e7eb;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .avatar-small img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 50%;
    }

    .avatar-small mat-icon {
      color: #6b7280;
      font-size: 24px;
    }

    .participante-info h3 {
      font-size: 1rem;
      font-weight: 600;
      color: #1f2937;
      margin: 0;
    }

    .tipo-usuario {
      font-size: 0.8rem;
      color: #6b7280;
      margin: 0;
    }

    .btn-opciones {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border: none;
      background: transparent;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .btn-opciones:hover {
      background: #f3f4f6;
    }

    .mensajes-area {
      flex: 1;
      overflow-y: auto;
      padding: 20px;
      background: #f9fafb;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .mensaje {
      display: flex;
      max-width: 70%;
    }

    .mensaje.propio {
      align-self: flex-end;
    }

    .mensaje-burbuja {
      background: white;
      padding: 12px 16px;
      border-radius: 16px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }

    .mensaje.propio .mensaje-burbuja {
      background: #4a90e2;
      color: white;
    }

    .mensaje-burbuja p {
      margin: 0 0 4px 0;
      font-size: 0.9rem;
      line-height: 1.5;
    }

    .hora {
      font-size: 0.7rem;
      opacity: 0.7;
    }

    .mensaje-input {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px 20px;
      border-top: 1px solid #e5e7eb;
      background: white;
    }

    .btn-adjuntar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border: none;
      background: #f3f4f6;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .btn-adjuntar:hover {
      background: #e5e7eb;
    }

    .mensaje-input input {
      flex: 1;
      padding: 12px 16px;
      border: 1px solid #e5e7eb;
      border-radius: 24px;
      font-size: 0.9rem;
      outline: none;
    }

    .mensaje-input input:focus {
      border-color: #4a90e2;
    }

    .btn-enviar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border: none;
      background: #4a90e2;
      color: white;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;
    }

    .btn-enviar:hover:not(:disabled) {
      background: #357abd;
      transform: scale(1.1);
    }

    .btn-enviar:disabled {
      background: #d1d5db;
      cursor: not-allowed;
    }

    .chat-vacio {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      color: #9ca3af;
    }

    .chat-vacio mat-icon {
      font-size: 80px;
      width: 80px;
      height: 80px;
      margin-bottom: 16px;
    }

    .chat-vacio h3 {
      font-size: 1.25rem;
      margin: 0 0 8px 0;
    }

    .chat-vacio p {
      margin: 0;
      font-size: 0.95rem;
    }

    @media (max-width: 768px) {
      .mensajes-container {
        grid-template-columns: 1fr;
      }

      .conversaciones-sidebar {
        display: none;
      }

      .conversaciones-sidebar.mobile-visible {
        display: flex;
      }

      .btn-volver-mobile {
        display: flex;
      }
    }
  `]
})
export class MensajesTerapeutaComponent implements OnInit {
  
  conversaciones = signal<Conversacion[]>([]);
  conversacionesFiltradas = signal<Conversacion[]>([]);
  conversacionActiva = signal<Conversacion | null>(null);
  mensajes = signal<Mensaje[]>([]);
  
  busquedaConversacion = '';
  nuevoMensajeTexto = '';

  constructor(
    private router: Router,
    private terapeutaService: TerapeutaService
  ) {}

  ngOnInit(): void {
    this.cargarConversaciones();
  }

  cargarConversaciones(): void {
    this.terapeutaService.obtenerConversaciones().subscribe({
      next: (conversaciones) => {
        this.conversaciones.set(conversaciones);
        this.conversacionesFiltradas.set(conversaciones);
      },
      error: (error) => {
        console.error('Error al cargar conversaciones:', error);
      }
    });
  }

  filtrarConversaciones(): void {
    const busqueda = this.busquedaConversacion.toLowerCase();
    const filtradas = this.conversaciones().filter(c =>
      c.nombre_participante.toLowerCase().includes(busqueda)
    );
    this.conversacionesFiltradas.set(filtradas);
  }

  seleccionarConversacion(conv: Conversacion): void {
    this.conversacionActiva.set(conv);
    this.cargarMensajes(conv.id_conversacion);
    
    // Marcar como leídos
    if (conv.no_leidos > 0) {
      this.terapeutaService.marcarMensajesLeidos(conv.id_conversacion).subscribe();
    }
  }

  cargarMensajes(idConversacion: number): void {
    this.terapeutaService.obtenerMensajesConversacion(idConversacion).subscribe({
      next: (mensajes) => {
        this.mensajes.set(mensajes);
      },
      error: (error) => {
        console.error('Error al cargar mensajes:', error);
      }
    });
  }

  enviarMensaje(): void {
    if (!this.nuevoMensajeTexto.trim() || !this.conversacionActiva()) return;

    const conv = this.conversacionActiva()!;
    
    this.terapeutaService.enviarMensaje(
      conv.tipo_participante,
      conv.id_conversacion,
      this.nuevoMensajeTexto
    ).subscribe({
      next: (mensaje) => {
        this.mensajes.update(msgs => [...msgs, mensaje]);
        this.nuevoMensajeTexto = '';
      },
      error: (error) => {
        console.error('Error al enviar mensaje:', error);
        alert('Error al enviar el mensaje');
      }
    });
  }

  nuevoMensaje(): void {
    console.log('Nuevo mensaje');
  }

  cerrarChat(): void {
    this.conversacionActiva.set(null);
  }

  getIconoTipo(tipo: string): string {
    const iconos: any = {
      'padre': 'family_restroom',
      'terapeuta': 'medical_services',
      'coordinador': 'admin_panel_settings'
    };
    return iconos[tipo] || 'person';
  }

  getTipoTexto(tipo: string): string {
    const textos: any = {
      'padre': 'Padre/Tutor',
      'terapeuta': 'Terapeuta',
      'coordinador': 'Coordinador'
    };
    return textos[tipo] || 'Usuario';
  }
}
