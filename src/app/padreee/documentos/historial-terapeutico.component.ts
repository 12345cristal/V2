import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-historial-terapeutico',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="historial-container">
      <h1>📊 Historial Terapéutico</h1>

      <div class="graficas-section">
        <h2>Visualización del Progreso</h2>

        <!-- Asistencia por mes -->
        <div class="grafica-card">
          <h3>📅 Asistencia por Mes</h3>
          <div class="grafica-placeholder">
            <p>Gráfica de barras: Sesiones asistidas por mes (Enero-Diciembre 2025)</p>
            <p style="font-size: 0.9rem; color: #999;">
              Enero: 4 | Febrero: 4 | Marzo: 3 | Abril: 4 | Mayo: 4 | Junio: 2
            </p>
          </div>
        </div>

        <!-- Sesiones realizadas vs canceladas -->
        <div class="grafica-card">
          <h3>✅ Sesiones Realizadas vs Canceladas</h3>
          <div class="grafica-placeholder">
            <p>Gráfica de pastel: Proporción de sesiones completadas</p>
            <p style="font-size: 0.9rem; color: #999;">
              Realizadas: 80% (25) | Canceladas: 20% (6)
            </p>
          </div>
        </div>

        <!-- Evolución de objetivos -->
        <div class="grafica-card">
          <h3>🎯 Evolución de Objetivos</h3>
          <div class="objetivos-list">
            <div class="objetivo-item">
              <div class="objetivo-header">
                <span class="objetivo-nombre">Mejora de socialización</span>
                <span class="objetivo-porcentaje">75%</span>
              </div>
              <div class="progreso-bar">
                <div class="progreso-fill" style="width: 75%; background: #2ecc71;"></div>
              </div>
            </div>

            <div class="objetivo-item">
              <div class="objetivo-header">
                <span class="objetivo-nombre">Control emocional</span>
                <span class="objetivo-porcentaje">60%</span>
              </div>
              <div class="progreso-bar">
                <div class="progreso-fill" style="width: 60%; background: #3498db;"></div>
              </div>
            </div>

            <div class="objetivo-item">
              <div class="objetivo-header">
                <span class="objetivo-nombre">Habilidades comunicacionales</span>
                <span class="objetivo-porcentaje">85%</span>
              </div>
              <div class="progreso-bar">
                <div class="progreso-fill" style="width: 85%; background: #9b59b6;"></div>
              </div>
            </div>

            <div class="objetivo-item">
              <div class="objetivo-header">
                <span class="objetivo-nombre">Independencia en tareas</span>
                <span class="objetivo-porcentaje">45%</span>
              </div>
              <div class="progreso-bar">
                <div class="progreso-fill" style="width: 45%; background: #f39c12;"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Frecuencia de terapias -->
        <div class="grafica-card">
          <h3>🏥 Frecuencia de Terapias</h3>
          <div class="terapias-list">
            <div class="terapia-item">
              <span class="terapia-nombre">Logopedia</span>
              <span class="terapia-frecuencia">2x por semana - 12 sesiones al mes</span>
            </div>
            <div class="terapia-item">
              <span class="terapia-nombre">Psicología</span>
              <span class="terapia-frecuencia">1x por semana - 4 sesiones al mes</span>
            </div>
            <div class="terapia-item">
              <span class="terapia-nombre">Terapia Ocupacional</span>
              <span class="terapia-frecuencia">1x por semana - 4 sesiones al mes</span>
            </div>
            <div class="terapia-item">
              <span class="terapia-nombre">Educación Física Adaptada</span>
              <span class="terapia-frecuencia">2x por semana - 8 sesiones al mes</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Resumen de avances -->
      <div class="resumen-section">
        <h2>📋 Resumen de Avances</h2>
        <div class="resumen-contenido">
          <p><strong>Período:</strong> Enero - Diciembre 2025</p>
          <p><strong>Total de sesiones programadas:</strong> 31</p>
          <p><strong>Total de sesiones realizadas:</strong> 25</p>
          <p><strong>Tasa de asistencia:</strong> 80.6%</p>
          <p><strong>Avance general:</strong> Muy Positivo ✅</p>
          
          <div class="observaciones">
            <h4>Observaciones principales:</h4>
            <ul>
              <li>El paciente ha mostrado un progreso significativo en habilidades de comunicación</li>
              <li>Ha mejorado su capacidad de socialización en pequeños grupos</li>
              <li>Se ha incrementado su independencia en actividades cotidianas</li>
              <li>Requiere continuar trabajando en control emocional en situaciones de estrés</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Descargas -->
      <div class="descargas-section">
        <h3>📥 Descargar Reportes</h3>
        <div class="botones-descarga">
          <button (click)="descargarReporteTerapeutico()" class="btn-descarga">
            📄 Descargar reporte terapéutico (PDF)
          </button>
          <button (click)="descargarResumenMensual()" class="btn-descarga">
            📊 Descargar resumen mensual (Excel)
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .historial-container {
      padding: 2rem;
      max-width: 1200px;
      margin: 0 auto;
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      min-height: 100vh;
    }

    h1 {
      color: #2c3e50;
      margin-bottom: 2rem;
      font-size: 2rem;
    }

    h2 {
      color: #2c3e50;
      margin: 2rem 0 1.5rem 0;
      font-size: 1.5rem;
    }

    h3 {
      color: #2c3e50;
      margin-top: 0;
    }

    h4 {
      color: #2c3e50;
      margin: 0.5rem 0;
    }

    /* Gráficas */
    .graficas-section {
      display: grid;
      gap: 2rem;
    }

    .grafica-card {
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      transition: all 0.3s;

      &:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
      }
    }

    .grafica-placeholder {
      background: #f8f9fa;
      border-radius: 8px;
      padding: 2rem;
      text-align: center;
      color: #7f8c8d;
      min-height: 200px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

      p {
        margin: 0.5rem 0;
      }
    }

    /* Objetivos */
    .objetivos-list {
      display: grid;
      gap: 1.5rem;
      margin-top: 1rem;
    }

    .objetivo-item {
      padding: 1rem;
      background: #f8f9fa;
      border-radius: 8px;
    }

    .objetivo-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }

    .objetivo-nombre {
      font-weight: 600;
      color: #2c3e50;
    }

    .objetivo-porcentaje {
      color: #3498db;
      font-weight: 700;
      font-size: 1.1rem;
    }

    .progreso-bar {
      width: 100%;
      height: 12px;
      background: #ecf0f1;
      border-radius: 6px;
      overflow: hidden;

      .progreso-fill {
        height: 100%;
        transition: width 0.3s ease;
      }
    }

    /* Terapias */
    .terapias-list {
      display: grid;
      gap: 1rem;
      margin-top: 1rem;
    }

    .terapia-item {
      background: #f8f9fa;
      padding: 1rem;
      border-radius: 8px;
      border-left: 4px solid #3498db;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .terapia-nombre {
      font-weight: 600;
      color: #2c3e50;
      flex: 1;
    }

    .terapia-frecuencia {
      color: #7f8c8d;
      font-size: 0.9rem;
      text-align: right;
    }

    /* Resumen */
    .resumen-section {
      background: white;
      border-radius: 12px;
      padding: 2rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      margin: 2rem 0;
    }

    .resumen-contenido {
      margin-top: 1rem;

      p {
        margin: 0.5rem 0;
        color: #555;

        strong {
          color: #2c3e50;
        }
      }
    }

    .observaciones {
      background: #ecf0f1;
      padding: 1rem;
      border-radius: 8px;
      margin-top: 1rem;

      ul {
        margin: 0.5rem 0 0 0;
        padding-left: 1.5rem;

        li {
          margin: 0.5rem 0;
          color: #555;
        }
      }
    }

    /* Descargas */
    .descargas-section {
      background: white;
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .botones-descarga {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1rem;
      margin-top: 1rem;
    }

    .btn-descarga {
      padding: 1rem;
      background: #3498db;
      color: white;
      border: none;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s;

      &:hover {
        background: #2980b9;
        transform: translateY(-2px);
      }
    }

    @media (max-width: 768px) {
      .historial-container {
        padding: 1rem;
      }

      h1 {
        font-size: 1.5rem;
      }

      .terapia-item {
        flex-direction: column;
        align-items: flex-start;
      }

      .terapia-frecuencia {
        margin-top: 0.5rem;
        text-align: left;
      }

      .botones-descarga {
        grid-template-columns: 1fr;
      }
    }
  `]
})
export class HistorialTerapeuticoComponent {
  descargarReporteTerapeutico() {
    alert('Descargando reporte terapéutico en PDF...');
  }

  descargarResumenMensual() {
    alert('Descargando resumen mensual en Excel...');
  }
}

export default HistorialTerapeuticoComponent;

