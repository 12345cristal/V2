import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface AccesibilidadConfig {
  textoGrande: boolean;
  coloresSuaves: boolean;
  modoLectura: boolean;
  contrasteAlto: boolean;
}

@Component({
  selector: 'app-perfil-accesibilidad',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="perfil-accesibilidad-container" [class.contraste-alto]="config.contrasteAlto">
      <div class="perfil-header">
        <h1>⚙️ Configuración de Accesibilidad</h1>
        <p class="subtitulo">Personaliza tu experiencia de navegación</p>
      </div>

      <div class="configuracion-section">
        <div class="opcion-accesibilidad">
          <div class="opcion-header">
            <span class="icono">🔠</span>
            <div class="opcion-info">
              <h3>Texto Grande</h3>
              <p>Aumenta el tamaño de la fuente en toda la aplicación</p>
            </div>
          </div>
          <label class="toggle-switch">
            <input type="checkbox" [(ngModel)]="config.textoGrande" (change)="guardarPreferencias()">
            <span class="slider"></span>
          </label>
        </div>

        <div class="opcion-accesibilidad">
          <div class="opcion-header">
            <span class="icono">🎨</span>
            <div class="opcion-info">
              <h3>Colores Suaves</h3>
              <p>Reduce la intensidad de los colores para mayor comodidad</p>
            </div>
          </div>
          <label class="toggle-switch">
            <input type="checkbox" [(ngModel)]="config.coloresSuaves" (change)="guardarPreferencias()">
            <span class="slider"></span>
          </label>
        </div>

        <div class="opcion-accesibilidad">
          <div class="opcion-header">
            <span class="icono">📖</span>
            <div class="opcion-info">
              <h3>Modo Lectura</h3>
              <p>Simplifica la interfaz mostrando solo contenido esencial</p>
            </div>
          </div>
          <label class="toggle-switch">
            <input type="checkbox" [(ngModel)]="config.modoLectura" (change)="guardarPreferencias()">
            <span class="slider"></span>
          </label>
        </div>

        <div class="opcion-accesibilidad">
          <div class="opcion-header">
            <span class="icono">🌙</span>
            <div class="opcion-info">
              <h3>Contraste Alto</h3>
              <p>Aumenta el contraste para mejor legibilidad</p>
            </div>
          </div>
          <label class="toggle-switch">
            <input type="checkbox" [(ngModel)]="config.contrasteAlto" (change)="guardarPreferencias()">
            <span class="slider"></span>
          </label>
        </div>
      </div>

      <!-- Perfil del usuario -->
      <div class="perfil-section">
        <h2>👤 Mi Perfil</h2>
        
        <div class="perfil-card">
          <div class="perfil-foto">
            <img src="assets/avatar-padre.jpg" alt="Tu foto">
          </div>

          <div class="perfil-info">
            <h3>{{ usuario.nombre }}</h3>
            <p class="email">{{ usuario.email }}</p>
            <p class="telefono">{{ usuario.telefono }}</p>
            
            <div class="perfil-datos">
              <div class="dato">
                <strong>Rol:</strong>
                <span>{{ usuario.rol }}</span>
              </div>
              <div class="dato">
                <strong>Hijo(s) a cargo:</strong>
                <span>{{ usuario.hijos.join(', ') }}</span>
              </div>
              <div class="dato">
                <strong>Miembro desde:</strong>
                <span>{{ usuario.fechaRegistro | date: 'longDate' }}</span>
              </div>
            </div>

            <button (click)="abrirEdicionPerfil()" class="btn-editar">
              ✏️ Editar Perfil
            </button>
          </div>
        </div>
      </div>

      <!-- Preferencias adicionales -->
      <div class="preferencias-section">
        <h2>🔔 Preferencias de Notificaciones</h2>
        
        <div class="preferencia-item">
          <label>
            <input type="checkbox" [(ngModel)]="notificaciones.nuevasSesiones">
            Notificarme de nuevas sesiones programadas
          </label>
        </div>

        <div class="preferencia-item">
          <label>
            <input type="checkbox" [(ngModel)]="notificaciones.comentarios">
            Notificarme de comentarios de terapeutas
          </label>
        </div>

        <div class="preferencia-item">
          <label>
            <input type="checkbox" [(ngModel)]="notificaciones.documentos">
            Notificarme de nuevos documentos
          </label>
        </div>

        <div class="preferencia-item">
          <label>
            <input type="checkbox" [(ngModel)]="notificaciones.pagos">
            Notificarme sobre pagos pendientes
          </label>
        </div>

        <button (click)="guardarPreferenciasNotificaciones()" class="btn-guardar">
          💾 Guardar Preferencias
        </button>
      </div>

      <!-- Otras opciones -->
      <div class="otras-opciones">
        <h2>Más Opciones</h2>
        
        <button class="btn-opcion">🔐 Cambiar Contraseña</button>
        <button class="btn-opcion">🗑️ Eliminar Cuenta</button>
        <button (click)="cerrarSesion()" class="btn-opcion btn-salir">🚪 Cerrar Sesión</button>
      </div>
    </div>
  `,
  styles: [`
    .perfil-accesibilidad-container {
      padding: 2rem;
      max-width: 1000px;
      margin: 0 auto;
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      min-height: 100vh;
      transition: all 0.3s;

      &.contraste-alto {
        background: #000;
        color: #fff;

        h1, h2, h3, p, label {
          color: #fff;
        }

        .opcion-accesibilidad, .perfil-card, .preferencia-item {
          background: #1a1a1a;
          border: 2px solid #fff;
        }
      }
    }

    .perfil-header {
      text-align: center;
      margin-bottom: 2rem;

      h1 {
        color: #2c3e50;
        margin: 0 0 0.5rem 0;
        font-size: 2rem;
      }

      .subtitulo {
        color: #7f8c8d;
        margin: 0;
      }
    }

    /* Configuración de accesibilidad */
    .configuracion-section {
      display: grid;
      gap: 1.5rem;
      margin-bottom: 2rem;
    }

    .opcion-accesibilidad {
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.3s;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
      }
    }

    .opcion-header {
      display: flex;
      gap: 1.5rem;
      align-items: center;
      flex: 1;

      .icono {
        font-size: 2rem;
        min-width: 50px;
        text-align: center;
      }
    }

    .opcion-info {
      h3 {
        margin: 0 0 0.25rem 0;
        color: #2c3e50;
      }

      p {
        margin: 0;
        color: #7f8c8d;
        font-size: 0.9rem;
      }
    }

    /* Toggle switch */
    .toggle-switch {
      position: relative;
      display: inline-block;
      width: 60px;
      height: 34px;

      input {
        opacity: 0;
        width: 0;
        height: 0;

        &:checked + .slider {
          background-color: #2ecc71;

          &:before {
            transform: translateX(26px);
          }
        }
      }
    }

    .slider {
      position: absolute;
      cursor: pointer;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: #ccc;
      transition: 0.4s;
      border-radius: 34px;

      &:before {
        position: absolute;
        content: "";
        height: 26px;
        width: 26px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        transition: 0.4s;
        border-radius: 50%;
      }
    }

    /* Perfil */
    .perfil-section {
      margin: 2rem 0;

      h2 {
        color: #2c3e50;
      }
    }

    .perfil-card {
      background: white;
      border-radius: 12px;
      padding: 2rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      display: grid;
      grid-template-columns: 150px 1fr;
      gap: 2rem;
      align-items: start;
    }

    .perfil-foto {
      img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #3498db;
      }
    }

    .perfil-info {
      h3 {
        margin: 0 0 0.5rem 0;
        color: #2c3e50;
        font-size: 1.5rem;
      }

      .email, .telefono {
        color: #7f8c8d;
        margin: 0.25rem 0;
      }
    }

    .perfil-datos {
      background: #f8f9fa;
      padding: 1rem;
      border-radius: 8px;
      margin: 1rem 0;

      .dato {
        margin: 0.75rem 0;

        strong {
          color: #2c3e50;
        }

        span {
          color: #555;
          margin-left: 0.5rem;
        }
      }
    }

    .btn-editar {
      padding: 0.75rem 1.5rem;
      background: #3498db;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.3s;

      &:hover {
        background: #2980b9;
        transform: translateY(-2px);
      }
    }

    /* Preferencias */
    .preferencias-section {
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      margin-bottom: 2rem;

      h2 {
        color: #2c3e50;
        margin-top: 0;
      }
    }

    .preferencia-item {
      padding: 0.75rem 0;

      label {
        display: flex;
        align-items: center;
        cursor: pointer;
        color: #555;

        input {
          margin-right: 1rem;
          cursor: pointer;
        }
      }
    }

    .btn-guardar {
      width: 100%;
      padding: 1rem;
      background: #2ecc71;
      color: white;
      border: none;
      border-radius: 8px;
      font-weight: 700;
      cursor: pointer;
      margin-top: 1rem;
      transition: all 0.3s;

      &:hover {
        background: #27ae60;
      }
    }

    /* Otras opciones */
    .otras-opciones {
      h2 {
        color: #2c3e50;
      }

      .btn-opcion {
        display: block;
        width: 100%;
        padding: 1rem;
        background: white;
        border: 2px solid #ecf0f1;
        border-radius: 8px;
        color: #2c3e50;
        font-weight: 600;
        cursor: pointer;
        margin-bottom: 1rem;
        transition: all 0.3s;

        &:hover {
          border-color: #3498db;
          background: #f8f9fa;
        }

        &.btn-salir {
          border-color: #e74c3c;
          color: #e74c3c;

          &:hover {
            background: #ffe5e5;
          }
        }
      }
    }

    @media (max-width: 768px) {
      .perfil-card {
        grid-template-columns: 1fr;
        text-align: center;

        .perfil-foto {
          justify-self: center;
        }
      }
    }
  `]
})
export class PerfilAccesibilidadComponent implements OnInit {
  config: AccesibilidadConfig = {
    textoGrande: false,
    coloresSuaves: false,
    modoLectura: false,
    contrasteAlto: false,
  };

  usuario = {
    nombre: 'María González',
    email: 'maria.gonzalez@email.com',
    telefono: '+57 (1) 2345-6789',
    rol: 'Madre/Padre',
    hijos: ['Juan Pérez', 'María Pérez'],
    fechaRegistro: new Date('2023-01-15'),
  };

  notificaciones = {
    nuevasSesiones: true,
    comentarios: true,
    documentos: true,
    pagos: true,
  };

  ngOnInit() {
    this.cargarPreferencias();
  }

  private cargarPreferencias() {
    const prefs = localStorage.getItem('accesibilidad');
    if (prefs) {
      this.config = JSON.parse(prefs);
    }
  }

  guardarPreferencias() {
    localStorage.setItem('accesibilidad', JSON.stringify(this.config));
    alert('Preferencias guardadas correctamente');
  }

  guardarPreferenciasNotificaciones() {
    localStorage.setItem('notificaciones', JSON.stringify(this.notificaciones));
    alert('Preferencias de notificaciones guardadas');
  }

  abrirEdicionPerfil() {
    alert('Abriendo editor de perfil...');
  }

  cerrarSesion() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
      alert('Cerrando sesión...');
    }
  }
}

export default PerfilAccesibilidadComponent;
