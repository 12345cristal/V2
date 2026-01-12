import { Component, signal, inject, effect, Input, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MensajesService } from '../../service/mensajes.service';
import { WebsocketService } from '../../service/websocket.service';
import { ChatListaItem, MensajeItem } from '../../interfaces/chat.interface';

@Component({
  selector: 'app-mensajes',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './mensajes.component.html',
  styleUrls: ['./mensajes.component.scss'],
})
export class MensajesComponent implements OnDestroy {
  @Input() ninoId: number | null = null;

  private svcMensajes = inject(MensajesService);
  private svcWebSocket = inject(WebsocketService);

  chats = signal<ChatListaItem[]>([]);
  chatActivoId = signal<number | null>(null);

  mensajes = signal<MensajeItem[]>([]);
  cargandoChats = signal<boolean>(false);
  cargandoMensajes = signal<boolean>(false);
  error = signal<string | null>(null);

  texto = signal<string>('');
  conectado = this.svcWebSocket.conectado;
  
  usuariosEscribiendo = signal<Map<number, string>>(new Map());
  usuariosConectados = signal<Set<number>>(new Set());

  // audio recording
  grabando = signal<boolean>(false);
  private mediaRecorder: MediaRecorder | null = null;
  private audioChunks: BlobPart[] = [];

  constructor() {
    effect(() => {
      this.cargarChats();
    });

    effect(() => {
      const id = this.chatActivoId();
      if (id) {
        this.conectarWebSocket(id);
        this.cargarMensajes(id);
      }
    });

    // Suscribirse a nuevos mensajes por WebSocket
    effect(() => {
      this.svcWebSocket.nuevoMensaje$.subscribe((mensaje) => {
        if (mensaje && mensaje.conversacionId === this.chatActivoId()) {
          this.mensajes.set([...this.mensajes(), mensaje]);
        }
      });
    });

    // Suscribirse a usuarios escribiendo
    effect(() => {
      this.svcWebSocket.usuarioEscribiendo$.subscribe((escribiendo) => {
        this.usuariosEscribiendo.set(escribiendo);
      });
    });

    // Suscribirse a usuarios conectados
    effect(() => {
      this.svcWebSocket.usuariosConectados$.subscribe((conectados) => {
        this.usuariosConectados.set(conectados);
      });
    });
  }

  cargarChats(): void {
    this.cargandoChats.set(true);
    this.error.set(null);

    this.svcMensajes.listarChats(this.ninoId ?? undefined).subscribe({
      next: (chats: ChatListaItem[]) => {
        this.chats.set(chats);
        this.cargandoChats.set(false);

        if (!this.chatActivoId() && chats.length > 0) {
          this.chatActivoId.set(chats[0].conversacionId);
        }
      },
      error: (err: Error) => {
        this.error.set('No se pudieron cargar los chats');
        this.cargandoChats.set(false);
        console.error('Error:', err);
      },
    });
  }

  seleccionarChat(id: number): void {
    if (this.chatActivoId() !== id) {
      this.chatActivoId.set(id);
    }
  }

  conectarWebSocket(conversacionId: number): void {
    this.svcWebSocket.conectar(conversacionId).catch((err) => {
      this.error.set('Error conectando a WebSocket');
      console.error('WebSocket error:', err);
    });
  }

  cargarMensajes(conversacionId: number): void {
    this.cargandoMensajes.set(true);
    this.error.set(null);

    this.svcMensajes.listarMensajes(conversacionId, 50).subscribe({
      next: (mensajes: MensajeItem[]) => {
        this.mensajes.set(mensajes);
        this.cargandoMensajes.set(false);

        // Marcar como visto
        this.svcMensajes.marcarVisto(conversacionId).subscribe({
          next: () => {},
          error: (err: Error) => console.error('Error al marcar visto:', err),
        });
      },
      error: (err: Error) => {
        this.error.set('No se pudieron cargar los mensajes');
        this.cargandoMensajes.set(false);
        console.error('Error:', err);
      },
    });
  }

  enviarTexto(): void {
    const id = this.chatActivoId();
    const t = this.texto().trim();

    if (!id || !t) return;

    // Usar WebSocket si está disponible, si no usar HTTP
    if (this.svcWebSocket.estaConectado()) {
      this.svcWebSocket.enviarMensaje(t);
      this.texto.set('');
      this.svcWebSocket.notificarDejoEscribiendo();
    } else {
      this.svcMensajes.enviarTexto(id, t).subscribe({
        next: (msg: MensajeItem) => {
          this.mensajes.set([...this.mensajes(), msg]);
          this.texto.set('');
          this.error.set(null);
        },
        error: (err: Error) => {
          this.error.set('No se pudo enviar el mensaje');
          console.error('Error:', err);
        },
      });
    }
  }

  onFileSelected(ev: Event): void {
    const id = this.chatActivoId();
    if (!id) return;

    const input = ev.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    this.svcMensajes.enviarArchivo(id, file).subscribe({
      next: (msg: MensajeItem) => {
        if (this.svcWebSocket.estaConectado()) {
          this.svcWebSocket.enviarArchivo(
            msg.archivoUrl || '',
            msg.archivoNombre || '',
            msg.tipo as 'ARCHIVO' | 'AUDIO'
          );
        }
        this.mensajes.set([...this.mensajes(), msg]);
        this.error.set(null);
      },
      error: (err: Error) => {
        this.error.set('No se pudo enviar el archivo');
        console.error('Error:', err);
      },
    });

    input.value = '';
  }

  async toggleGrabacion(): Promise<void> {
    const id = this.chatActivoId();
    if (!id) return;

    if (!this.grabando()) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.audioChunks = [];
        this.mediaRecorder = new MediaRecorder(stream);

        this.mediaRecorder.ondataavailable = (e: BlobEvent) => {
          this.audioChunks.push(e.data);
        };

        this.mediaRecorder.onstop = () => {
          const blob = new Blob(this.audioChunks, { type: 'audio/webm' });
          this.svcMensajes.enviarAudio(id, blob).subscribe({
            next: (msg: MensajeItem) => {
              if (this.svcWebSocket.estaConectado()) {
                this.svcWebSocket.enviarArchivo(
                  msg.archivoUrl || '',
                  msg.archivoNombre || '',
                  'AUDIO'
                );
              }
              this.mensajes.set([...this.mensajes(), msg]);
              this.error.set(null);
            },
            error: (err: Error) => {
              this.error.set('No se pudo enviar el audio');
              console.error('Error:', err);
            },
          });
          stream.getTracks().forEach((t) => t.stop());
        };

        this.mediaRecorder.start();
        this.grabando.set(true);
      } catch (err) {
        this.error.set('No se pudo acceder al micrófono');
        console.error('Microphone error:', err);
      }
    } else {
      if (this.mediaRecorder) {
        this.mediaRecorder.stop();
      }
      this.grabando.set(false);
    }
  }

  onInputChange(): void {
    if (this.svcWebSocket.estaConectado()) {
      this.svcWebSocket.notificarEscribiendo();
    }
  }

  ngOnDestroy(): void {
    this.svcWebSocket.desconectar();
  }
}
