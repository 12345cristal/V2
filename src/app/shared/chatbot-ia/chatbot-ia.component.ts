// src/app/shared/chatbot-ia/chatbot-ia.component.ts
import { CommonModule } from '@angular/common';
import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
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
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot-ia.component.html',
  styleUrls: ['./chatbot-ia.component.scss']
})
export class ChatbotIaComponent implements OnInit {
  @Input() ninoId?: number;
  @Input() incluirContexto = true;

  @ViewChild('mensajesRef') mensajesRef?: ElementRef<HTMLDivElement>;

  mensajes: MensajeUI[] = [];
  mensajeActual = '';
  cargando = false;
  chatAbierto = false;

  geminiConfigurado = true;
  private sessionId?: string;

  preguntasSugeridas = [
    '¿Cómo puedo mejorar la comunicación con mi hijo?',
    '¿Qué actividades son recomendadas para niños con TEA?',
    '¿Cómo manejar las rabietas?',
    'Consejos para establecer rutinas',
    '¿Qué terapias suelen apoyar más?'
  ];

  constructor(private gemini: GeminiIaService) {
    this.agregarMensajeBienvenida();
  }

  ngOnInit(): void {
    this.verificarEstado();
  }

  verificarEstado(): void {
    this.gemini.verificarEstado().subscribe({
      next: (estado) => {
        this.geminiConfigurado = estado.configurado;
        if (!this.geminiConfigurado) {
          console.warn('⚠️ Gemini no configurado');
        }
      },
      error: (err) => {
        console.error('Error verificando estado:', err);
        this.geminiConfigurado = false;
      }
    });
  }

  toggleChat(): void {
    this.chatAbierto = !this.chatAbierto;
    if (this.chatAbierto) {
      this.scrollToBottom();
    }
  }

  limpiarChat(): void {
    this.mensajes = [];
    this.sessionId = undefined;
    this.agregarMensajeBienvenida();
  }

  usarPreguntaSugerida(pregunta: string): void {
    this.mensajeActual = pregunta;
    this.enviarMensaje();
  }

  enviarMensaje(): void {
    const msg = this.mensajeActual.trim();
    if (!msg || this.cargando) return;

    // Agregar mensaje del usuario
    this.mensajes.push({
      texto: msg,
      esUsuario: true,
      timestamp: new Date()
    });

    this.mensajeActual = '';
    this.cargando = true;
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
          this.sessionId = respuesta.session_id;
          this.mensajes.push({
            texto: respuesta.respuesta,
            esUsuario: false,
            timestamp: new Date(),
            contextoUsado: respuesta.contexto_usado
          });
          this.cargando = false;
          this.scrollToBottom();
        },
        error: (err) => {
          console.error('Error en chatbot:', err);
          this.cargando = false;
          this.mensajes.push({
            texto: 'Hubo un error procesando tu consulta. Por favor, intenta de nuevo. Si persiste, revisa la conexión o configuración de IA.',
            esUsuario: false,
            timestamp: new Date()
          });
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
    this.mensajes.push({
      texto: '¡Hola! 👋 Soy tu asistente IA para dudas sobre TEA y terapias. ¿Qué te gustaría preguntar?',
      esUsuario: false,
      timestamp: new Date()
    });
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      const el = this.mensajesRef?.nativeElement;
      if (!el) return;
      el.scrollTop = el.scrollHeight;
    }, 50);
  }
}
