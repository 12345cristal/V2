import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface Mensaje {
  id: string;
  remitente: string;
  contenido: string;
  tipo: 'texto' | 'audio' | 'archivo';
  fecha: Date;
  leido: boolean;
}

interface Chat {
  id: string;
  nombre: string;
  tipo: 'terapeuta' | 'coordinador' | 'administrador';
  ultimoMensaje: string;
  ultimaFecha: Date;
  noLeidos: number;
  mensajes: Mensaje[];
}

@Component({
  selector: 'app-mensajes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="mensajes-container">
      <h1>💬 Mensajes con el Equipo</h1>

      <div class="mensajes-layout">
        <!-- Lista de chats -->
        <div class="chats-list">
          <h3>Conversaciones</h3>
          <div class="chat-item"
               *ngFor="let chat of chats"
               (click)="seleccionarChat(chat)"
               [class.activo]="chatSeleccionado?.id === chat.id">
            <div class="chat-header">
              <span class="chat-nombre">{{ chat.nombre }}</span>
              <span class="badge" *ngIf="chat.noLeidos > 0">
                {{ chat.noLeidos }}
              </span>
            </div>
            <p class="ultimo-mensaje">{{ chat.ultimoMensaje }}</p>
            <small>{{ chat.ultimaFecha | date: 'short' }}</small>
          </div>
        </div>

        <!-- Panel de chat -->
        <div class="chat-panel" *ngIf="chatSeleccionado">
          <div class="chat-header-main">
            <h2>{{ chatSeleccionado.nombre }}</h2>
            <small>{{ chatSeleccionado.tipo | uppercase }}</small>
          </div>

          <div class="mensajes-area">
            <div *ngFor="let msg of chatSeleccionado.mensajes"
                 class="mensaje"
                 [class.propio]="msg.remitente === 'Yo'">
              <div class="mensaje-contenido">
                <p class="remitente" *ngIf="msg.remitente !== 'Yo'">
                  {{ msg.remitente }}
                </p>
                <div class="mensaje-bubble">
                  <p *ngIf="msg.tipo === 'texto'">{{ msg.contenido }}</p>
                  <p *ngIf="msg.tipo === 'audio'" class="archivo">🎤 Mensaje de audio</p>
                  <p *ngIf="msg.tipo === 'archivo'" class="archivo">📎 {{ msg.contenido }}</p>
                </div>
                <small>{{ msg.fecha | date: 'short' }}</small>
              </div>
            </div>
          </div>

          <div class="entrada-mensaje">
            <input type="text" 
                   placeholder="Escribe tu mensaje..."
                   [(ngModel)]="nuevoMensaje"
                   (keyup.enter)="enviarMensaje()">
            <button (click)="enviarMensaje()" class="btn-enviar">Enviar</button>
            <button class="btn-archivo">📎</button>
            <button class="btn-audio">🎤</button>
          </div>
        </div>

        <div *ngIf="!chatSeleccionado" class="sin-chat">
          <p>Selecciona una conversación para empezar</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .mensajes-container {
      padding: 2rem;
      height: calc(100vh - 100px);
      display: flex;
      flex-direction: column;
    }

    h1 {
      color: #2c3e50;
      margin: 0 0 1.5rem 0;
    }

    .mensajes-layout {
      display: grid;
      grid-template-columns: 300px 1fr;
      gap: 1rem;
      flex: 1;
      min-height: 0;

      @media (max-width: 768px) {
        grid-template-columns: 1fr;
      }
    }

    /* Lista de chats */
    .chats-list {
      background: white;
      border-radius: 12px;
      padding: 1rem;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      overflow-y: auto;

      h3 {
        margin: 0 0 1rem 0;
        color: #2c3e50;
      }
    }

    .chat-item {
      padding: 1rem;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
      border-left: 3px solid transparent;

      &:hover {
        background: #f8f9fa;
      }

      &.activo {
        background: #ecf0f1;
        border-left-color: #3498db;
      }
    }

    .chat-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }

    .chat-nombre {
      font-weight: 600;
      color: #2c3e50;
    }

    .badge {
      background: #e74c3c;
      color: white;
      padding: 0.25rem 0.5rem;
      border-radius: 10px;
      font-size: 0.75rem;
      font-weight: 700;
    }

    .ultimo-mensaje {
      margin: 0.25rem 0;
      color: #7f8c8d;
      font-size: 0.9rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    small {
      color: #95a5a6;
      font-size: 0.8rem;
    }

    /* Chat panel */
    .chat-panel {
      background: white;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      display: flex;
      flex-direction: column;
      min-height: 0;
    }

    .chat-header-main {
      padding: 1rem;
      border-bottom: 1px solid #ecf0f1;

      h2 {
        margin: 0 0 0.25rem 0;
        color: #2c3e50;
      }

      small {
        color: #7f8c8d;
      }
    }

    .mensajes-area {
      flex: 1;
      overflow-y: auto;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .mensaje {
      display: flex;
      justify-content: flex-start;

      &.propio {
        justify-content: flex-end;

        .mensaje-contenido {
          align-items: flex-end;
        }

        .mensaje-bubble {
          background: #3498db;
          color: white;
        }
      }
    }

    .mensaje-contenido {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      max-width: 70%;
    }

    .remitente {
      margin: 0 0 0.25rem 0;
      font-weight: 600;
      font-size: 0.85rem;
      color: #7f8c8d;
    }

    .mensaje-bubble {
      background: #ecf0f1;
      padding: 0.75rem 1rem;
      border-radius: 12px;
      color: #2c3e50;

      p {
        margin: 0;
      }

      &.archivo {
        color: #3498db;
        font-weight: 500;
      }
    }

    /* Entrada de mensaje */
    .entrada-mensaje {
      padding: 1rem;
      border-top: 1px solid #ecf0f1;
      display: flex;
      gap: 0.5rem;

      input {
        flex: 1;
        padding: 0.75rem;
        border: 1px solid #ecf0f1;
        border-radius: 8px;
        font-size: 0.95rem;

        &:focus {
          outline: none;
          border-color: #3498db;
        }
      }
    }

    .btn-enviar, .btn-archivo, .btn-audio {
      padding: 0.75rem 1rem;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.2s;
    }

    .btn-enviar {
      background: #3498db;
      color: white;

      &:hover {
        background: #2980b9;
      }
    }

    .btn-archivo, .btn-audio {
      background: #ecf0f1;
      color: #2c3e50;
      width: 44px;
      padding: 0;
      font-size: 1rem;

      &:hover {
        background: #d5dbdb;
      }
    }

    .sin-chat {
      display: flex;
      align-items: center;
      justify-content: center;
      background: white;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      grid-column: 2;
      color: #95a5a6;

      @media (max-width: 768px) {
        grid-column: 1;
      }
    }

    @media (max-width: 768px) {
      .chats-list {
        display: none;
      }

      .mensajes-area {
        max-height: 400px;
      }
    }
  `]
})
export class MensajesComponent implements OnInit {
  chats: Chat[] = [];
  chatSeleccionado: Chat | null = null;
  nuevoMensaje: string = '';

  ngOnInit() {
    this.cargarChats();
  }

  private cargarChats() {
    this.chats = [
      {
        id: '1',
        nombre: 'Dra. María García',
        tipo: 'terapeuta',
        ultimoMensaje: 'El niño progresa muy bien en las sesiones',
        ultimaFecha: new Date('2026-01-10'),
        noLeidos: 2,
        mensajes: [
          {
            id: '1',
            remitente: 'Dra. María García',
            contenido: '¿Cómo está Juan en casa?',
            tipo: 'texto',
            fecha: new Date('2026-01-09'),
            leido: true,
          },
          {
            id: '2',
            remitente: 'Yo',
            contenido: 'Muy bien, realizando las tareas',
            tipo: 'texto',
            fecha: new Date('2026-01-09'),
            leido: true,
          },
          {
            id: '3',
            remitente: 'Dra. María García',
            contenido: 'El niño progresa muy bien en las sesiones',
            tipo: 'texto',
            fecha: new Date('2026-01-10'),
            leido: false,
          },
        ],
      },
      {
        id: '2',
        nombre: 'Coordinadora',
        tipo: 'coordinador',
        ultimoMensaje: 'Confirma la sesión de mañana',
        ultimaFecha: new Date('2026-01-11'),
        noLeidos: 1,
        mensajes: [
          {
            id: '1',
            remitente: 'Coordinadora',
            contenido: 'Confirma la sesión de mañana a las 10 AM',
            tipo: 'texto',
            fecha: new Date('2026-01-11'),
            leido: false,
          },
        ],
      },
    ];
  }

  seleccionarChat(chat: Chat) {
    this.chatSeleccionado = chat;
    chat.noLeidos = 0;
  }

  enviarMensaje() {
    if (!this.nuevoMensaje.trim() || !this.chatSeleccionado) return;

    const mensaje: Mensaje = {
      id: Date.now().toString(),
      remitente: 'Yo',
      contenido: this.nuevoMensaje,
      tipo: 'texto',
      fecha: new Date(),
      leido: true,
    };

    this.chatSeleccionado.mensajes.push(mensaje);
    this.nuevoMensaje = '';
  }
}

export default MensajesComponent;

