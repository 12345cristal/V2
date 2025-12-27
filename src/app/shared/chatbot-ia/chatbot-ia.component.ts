// src/app/shared/chatbot-ia/chatbot-ia.component.ts
import { Component, ElementRef, Input, OnInit, ViewChild, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { GeminiIaService, ChatbotResponse } from '../../service/gemini-ia.service';

interface MensajeUI {
  texto: string;
  esUsuario: boolean;
  timestamp: Date;
  contextoUsado?: boolean;
}

@Component({
  selector: 'app-chatbot-ia',
  standalone: true,
  imports: [FormsModule, DatePipe],
  templateUrl: './chatbot-ia.component.html',
  styleUrls: ['./chatbot-ia.component.scss']
})
export class ChatbotIaComponent implements OnInit {
  @Input() ninoId?: number;
  @Input() incluirContexto = true;

  @ViewChild('mensajesRef') mensajesRef?: ElementRef<HTMLDivElement>;

  mensajes = signal<MensajeUI[]>([]);
  mensajeActual = signal('');
  cargando = signal(false);
  chatAbierto = signal(false);

  geminiConfigurado = signal(true);
  private sessionId?: string;

  preguntasSugeridas = [
    '¿Cómo puedo mejorar la comunicación con mi hijo?',
    '¿Qué actividades son recomendadas para niños con TEA?',
    '¿Cómo manejar las rabietas?',
    'Consejos para establecer rutinas',
    '¿Qué terapias suelen apoyar más?'
  ];

  constructor(
    private gemini: GeminiIaService
  ) {
    this.agregarMensajeBienvenida();
  }

  ngOnInit(): void {
    this.verificarEstado();
  }

  verificarEstado(): void {
    this.gemini.verificarEstado().subscribe({
      next: (estado) => {
        this.geminiConfigurado.set(estado.configurado);
        if (!estado.configurado) {
          console.warn('⚠️ Gemini no configurado');
        }
      },
      error: (err) => {
        console.error('Error verificando estado:', err);
        this.geminiConfigurado.set(false);
      }
    });
  }

  toggleChat(): void {
    this.chatAbierto.update(v => !v);
    if (this.chatAbierto()) {
      this.scrollToBottom();
    }
  }

  limpiarChat(): void {
    this.mensajes.set([]);
    this.sessionId = undefined;
    this.agregarMensajeBienvenida();
  }

  usarPreguntaSugerida(pregunta: string): void {
    this.mensajeActual.set(pregunta);
    this.enviarMensaje();
  }

  enviarMensaje(): void {
    const msg = this.mensajeActual().trim();
    if (!msg || this.cargando()) return;

    console.log('🚀 ENVIANDO MENSAJE:', msg);

    // Agregar mensaje del usuario
    this.mensajes.update(msgs => [...msgs, {
      texto: msg,
      esUsuario: true,
      timestamp: new Date()
    }]);

    this.mensajeActual.set('');
    this.cargando.set(true);
    this.scrollToBottom();

    // Función para enviar el mensaje
    const send = () => {
      this.gemini.chatbot({
        mensaje: msg,
        nino_id: this.ninoId,
        incluir_contexto: this.incluirContexto && !!this.ninoId,
        session_id: this.sessionId
      }).subscribe({
        next: (respuesta: ChatbotResponse) => {
          console.log('✅ RESPUESTA COMPLETA BACKEND:', respuesta);
          console.log('📝 TEXTO RESPUESTA:', respuesta.respuesta);
          console.log('📏 LONGITUD:', respuesta.respuesta?.length);
          
          this.sessionId = respuesta.session_id;
          
          const nuevoMensaje: MensajeUI = {
            texto: respuesta.respuesta,
            esUsuario: false,
            timestamp: new Date(),
            contextoUsado: respuesta.contexto_usado
          };
          
          this.mensajes.update(msgs => [...msgs, nuevoMensaje]);
          
          console.log('💬 MENSAJE AGREGADO, TOTAL MENSAJES:', this.mensajes().length);
          console.log('📋 ARRAY MENSAJES:', this.mensajes());
          
          this.cargando.set(false);
          this.scrollToBottom();
        },
        error: (err) => {
          console.error('❌ ERROR EN CHATBOT:', err);
          this.cargando.set(false);
          this.mensajes.update(msgs => [...msgs, {
            texto: 'Hubo un error procesando tu consulta. Por favor, intenta de nuevo. Si persiste, revisa la conexión o configuración de IA.',
            esUsuario: false,
            timestamp: new Date()
          }]);
          this.scrollToBottom();
        }
      });
    };

    // Si no hay sesión, crearla primero
    if (!this.sessionId) {
      this.gemini.iniciarSesion().subscribe({
        next: (res) => {
          this.sessionId = res.session_id;
          send();
        },
        error: () => {
          // Fallback: enviar sin sesión previa
          send();
        }
      });
    } else {
      send();
    }
  }

  private agregarMensajeBienvenida(): void {
    this.mensajes.set([{
      texto: '¡Hola! 👋 Soy tu asistente IA para dudas sobre TEA y terapias. ¿Qué te gustaría preguntar?',
      esUsuario: false,
      timestamp: new Date()
    }]);
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      const el = this.mensajesRef?.nativeElement;
      if (!el) return;
      el.scrollTop = el.scrollHeight;
    }, 50);
  }

  formatTexto(texto: string): string {
    return texto
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>');
  }
}
