// src/app/shared/chatbot-ia/chatbot-ia.component.ts
import { Component, Input, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GeminiIaService, ChatbotResponse } from '../../service/gemini-ia.service';

interface Mensaje {
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
  @Input() incluirContexto: boolean = true;
  
  mensajes: Mensaje[] = [];
  mensajeActual: string = '';
  cargando: boolean = false;
  chatAbierto: boolean = false;
  geminiConfigurado: boolean = true;

  preguntasSugeridas = [
    '¿Cómo puedo mejorar la comunicación con mi hijo?',
    '¿Qué actividades son recomendadas para niños con TEA?',
    '¿Cómo manejar las rabietas?',
    'Dame consejos para establecer rutinas',
    '¿Qué terapias son más efectivas?'
  ];

  constructor(private geminiService: GeminiIaService) {}

  ngOnInit(): void {
    this.verificarEstado();
    this.agregarMensajeBienvenida();
  }

  verificarEstado(): void {
    this.geminiService.verificarEstado().subscribe({
      next: (estado) => {
        this.geminiConfigurado = estado.configurado;
        if (!this.geminiConfigurado) {
          this.mensajes.push({
            texto: '⚠️ El chatbot de IA no está configurado completamente. Las respuestas pueden ser limitadas.',
            esUsuario: false,
            timestamp: new Date()
          });
        }
      },
      error: () => {
        this.geminiConfigurado = false;
      }
    });
  }

  agregarMensajeBienvenida(): void {
    this.mensajes.push({
      texto: '¡Hola! 👋 Soy tu asistente virtual especializado en autismo y terapias. ¿En qué puedo ayudarte hoy?',
      esUsuario: false,
      timestamp: new Date()
    });
  }

  toggleChat(): void {
    this.chatAbierto = !this.chatAbierto;
  }

  enviarMensaje(): void {
    if (!this.mensajeActual.trim() || this.cargando) return;

    // Agregar mensaje del usuario
    const mensajeUsuario = this.mensajeActual.trim();
    this.mensajes.push({
      texto: mensajeUsuario,
      esUsuario: true,
      timestamp: new Date()
    });

    this.mensajeActual = '';
    this.cargando = true;

    // Enviar al chatbot
    this.geminiService.chatbot({
      mensaje: mensajeUsuario,
      nino_id: this.ninoId,
      incluir_contexto: this.incluirContexto && !!this.ninoId
    }).subscribe({
      next: (response: ChatbotResponse) => {
        this.mensajes.push({
          texto: response.respuesta,
          esUsuario: false,
          timestamp: new Date(),
          contextoUsado: response.contexto_usado
        });
        this.cargando = false;
        this.scrollToBottom();
      },
      error: (error) => {
        this.mensajes.push({
          texto: 'Lo siento, hubo un error procesando tu consulta. Por favor, intenta nuevamente.',
          esUsuario: false,
          timestamp: new Date()
        });
        this.cargando = false;
        console.error('Error en chatbot:', error);
      }
    });
  }

  usarPreguntaSugerida(pregunta: string): void {
    this.mensajeActual = pregunta;
    this.enviarMensaje();
  }

  limpiarChat(): void {
    this.mensajes = [];
    this.agregarMensajeBienvenida();
  }

  scrollToBottom(): void {
    setTimeout(() => {
      const chatContainer = document.querySelector('.chat-mensajes');
      if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }
    }, 100);
  }
}
