import {
  Component,
  signal,
  inject,
  effect,
  Input,
  OnDestroy,
} from '@angular/core';
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
  cargandoChats = signal(false);
  cargandoMensajes = signal(false);
  error = signal<string | null>(null);

  texto = signal('');
  conectado = this.svcWebSocket.conectado;

  usuariosEscribiendo = signal<Map<number, string>>(new Map());
  usuariosConectados = signal<Set<number>>(new Set());

  // Audio
  grabando = signal(false);
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

    this.svcWebSocket.nuevoMensaje$.subscribe((mensaje) => {
      if (mensaje && mensaje.conversacionId === this.chatActivoId()) {
        this.mensajes.set([...this.mensajes(), mensaje]);
      }
    });

    this.svcWebSocket.usuarioEscribiendo$.subscribe((mapa) => {
      this.usuariosEscribiendo.set(mapa);
    });

    this.svcWebSocket.usuariosConectados$.subscribe((set) => {
      this.usuariosConectados.set(set);
    });
  }

  // ==========================
  // INPUT TEXTO
  // ==========================
  onInput(event: Event): void {
    const value = (event.target as HTMLInputElement).value;
    this.texto.set(value);
    this.onInputChange();
  }

  onInputChange(): void {
    if (this.svcWebSocket.estaConectado()) {
      this.svcWebSocket.notificarEscribiendo();
    }
  }

  // ==========================
  // CHATS
  // ==========================
  cargarChats(): void {
    this.cargandoChats.set(true);
    this.error.set(null);

    this.svcMensajes.listarChats(this.ninoId ?? undefined).subscribe({
      next: (chats) => {
        this.chats.set(chats);
        this.cargandoChats.set(false);

        if (!this.chatActivoId() && chats.length > 0) {
          this.chatActivoId.set(chats[0].conversacionId);
        }
      },
      error: (err) => {
        this.error.set('No se pudieron cargar los chats');
        this.cargandoChats.set(false);
        console.error(err);
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
      console.error(err);
    });
  }

  cargarMensajes(conversacionId: number): void {
    this.cargandoMensajes.set(true);
    this.error.set(null);

    this.svcMensajes.listarMensajes(conversacionId, 50).subscribe({
      next: (mensajes) => {
        this.mensajes.set(mensajes);
        this.cargandoMensajes.set(false);
        this.svcMensajes.marcarVisto(conversacionId).subscribe();
      },
      error: (err) => {
        this.error.set('No se pudieron cargar los mensajes');
        this.cargandoMensajes.set(false);
        console.error(err);
      },
    });
  }

  // ==========================
  // ENVIAR TEXTO
  // ==========================
  enviarTexto(): void {
    const id = this.chatActivoId();
    const texto = this.texto().trim();

    if (!id || !texto) return;

    if (this.svcWebSocket.estaConectado()) {
      this.svcWebSocket.enviarMensaje(texto);
      this.texto.set('');
      this.svcWebSocket.notificarEscribiendo();
      return;
    }

    this.svcMensajes.enviarTexto(id, texto).subscribe({
      next: (msg) => {
        this.mensajes.set([...this.mensajes(), msg]);
        this.texto.set('');
      },
      error: (err) => {
        this.error.set('No se pudo enviar el mensaje');
        console.error(err);
      },
    });
  }

  // ==========================
  // ARCHIVOS
  // ==========================
  onFileSelected(ev: Event): void {
    const id = this.chatActivoId();
    if (!id) return;

    const input = ev.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    this.svcMensajes.enviarArchivo(id, file).subscribe({
      next: (msg) => {
        this.mensajes.set([...this.mensajes(), msg]);
      },
      error: (err) => {
        this.error.set('No se pudo enviar el archivo');
        console.error(err);
      },
    });

    input.value = '';
  }

  // ==========================
  // AUDIO
  // ==========================
  async toggleGrabacion(): Promise<void> {
    const id = this.chatActivoId();
    if (!id) return;

    if (!this.grabando()) {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.audioChunks = [];
      this.mediaRecorder = new MediaRecorder(stream);

      this.mediaRecorder.ondataavailable = (e) =>
        this.audioChunks.push(e.data);

      this.mediaRecorder.onstop = () => {
        const blob = new Blob(this.audioChunks, { type: 'audio/webm' });
this.svcMensajes.enviarAudio(id, blob).subscribe((msg: MensajeItem) => {
          this.mensajes.set([...this.mensajes(), msg]);
        });
        stream.getTracks().forEach((t) => t.stop());
      };

      this.mediaRecorder.start();
      this.grabando.set(true);
    } else {
      this.mediaRecorder?.stop();
      this.grabando.set(false);
    }
  }

  ngOnDestroy(): void {
    this.svcWebSocket.desconectar();
  }
}
