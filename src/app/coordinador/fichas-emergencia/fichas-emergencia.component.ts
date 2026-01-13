// src/app/coordinador/fichas-emergencia/fichas-emergencia.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { FichasEmergenciaService, FichaEmergencia } from '../../service/fichas-emergencia.service';

@Component({
  selector: 'app-fichas-emergencia',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './fichas-emergencia.component.html',
  styleUrls: ['./fichas-emergencia.component.scss']
})
export class FichasEmergenciaComponent implements OnInit {
  fichas: FichaEmergencia[] = [];
  fichasFiltradas: FichaEmergencia[] = [];
  cargando: boolean = false;
  error: string = '';
  
  // Filtros
  busqueda: string = '';
  filtroEstado: string = 'TODOS';

  constructor(
    private fichasService: FichasEmergenciaService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.cargarFichas();
  }

  cargarFichas(): void {
    this.cargando = true;
    this.error = '';
    
    this.fichasService.listarFichas().subscribe({
      next: (fichas) => {
        this.fichas = fichas;
        this.aplicarFiltros();
        this.cargando = false;
      },
      error: (err) => {
        console.error('Error cargando fichas:', err);
        this.error = 'Error al cargar las fichas de emergencia';
        this.cargando = false;
      }
    });
  }

  aplicarFiltros(): void {
    let resultado = [...this.fichas];

    // Filtro por búsqueda
    if (this.busqueda.trim()) {
      const termino = this.busqueda.toLowerCase();
      resultado = resultado.filter(f => 
        f.nino_nombre_completo?.toLowerCase().includes(termino) ||
        f.diagnostico_principal?.toLowerCase().includes(termino) ||
        f.contacto_principal_nombre?.toLowerCase().includes(termino)
      );
    }

    // Filtro por estado del niño
    if (this.filtroEstado !== 'TODOS') {
      resultado = resultado.filter(f => f.nino_estado === this.filtroEstado);
    }

    this.fichasFiltradas = resultado;
  }

  verFicha(ninoId: number): void {
    this.router.navigate(['/coordinador/fichas-emergencia', ninoId]);
  }

  imprimirFicha(ninoId: number): void {
    this.fichasService.obtenerFichaImprimible(ninoId).subscribe({
      next: (ficha) => {
        // Abrir en nueva ventana para imprimir
        const ventana = window.open('', '_blank');
        if (ventana) {
          ventana.document.write(this.generarHTMLImpresion(ficha));
          ventana.document.close();
          setTimeout(() => {
            ventana.print();
          }, 500);
        }
      },
      error: (err) => {
        console.error('Error obteniendo ficha imprimible:', err);
        alert('Error al generar ficha para impresión');
      }
    });
  }

  private generarHTMLImpresion(ficha: any): string {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Ficha de Emergencia - ${ficha.nino_nombre_completo}</title>
        <style>
          @media print {
            @page { margin: 1cm; }
          }
          body {
            font-family: Arial, sans-serif;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
          }
          .header {
            background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
          }
          .header h1 {
            margin: 0 0 5px 0;
            font-size: 24px;
          }
          .header p {
            margin: 0;
            opacity: 0.9;
          }
          .foto {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            border: 4px solid white;
            margin: 10px auto;
            display: block;
          }
          .seccion {
            margin-bottom: 20px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            padding: 15px;
          }
          .seccion h2 {
            margin: 0 0 15px 0;
            font-size: 18px;
            color: #dc2626;
            border-bottom: 2px solid #dc2626;
            padding-bottom: 8px;
          }
          .campo {
            margin-bottom: 10px;
          }
          .campo strong {
            display: inline-block;
            width: 200px;
            color: #374151;
          }
          .campo span {
            color: #1f2937;
          }
          .emergencia {
            background: #fef2f2;
            border-left: 4px solid #dc2626;
            padding: 15px;
            margin: 10px 0;
            font-weight: 500;
          }
          .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #e5e7eb;
            font-size: 12px;
            color: #6b7280;
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>⚠️ FICHA DE EMERGENCIA</h1>
          <p>Información crítica para situaciones de emergencia</p>
        </div>

        ${ficha.nino_foto_url ? `<img src="${ficha.nino_foto_url}" class="foto" alt="Foto">` : ''}

        <div class="seccion">
          <h2>👤 Datos del Niño</h2>
          <div class="campo"><strong>Nombre completo:</strong> <span>${ficha.nino_nombre_completo}</span></div>
          <div class="campo"><strong>Edad:</strong> <span>${ficha.nino_edad} años</span></div>
          <div class="campo"><strong>Sexo:</strong> <span>${ficha.nino_sexo === 'M' ? 'Masculino' : ficha.nino_sexo === 'F' ? 'Femenino' : 'Otro'}</span></div>
          <div class="campo"><strong>Fecha de nacimiento:</strong> <span>${ficha.nino_fecha_nacimiento || 'No especificada'}</span></div>
        </div>

        <div class="seccion">
          <h2>🩸 Información Médica Crítica</h2>
          <div class="campo"><strong>Tipo de sangre:</strong> <span style="font-size: 20px; font-weight: bold; color: #dc2626;">${ficha.tipo_sangre || 'NO ESPECIFICADO'}</span></div>
          <div class="campo"><strong>Diagnóstico:</strong> <span>${ficha.diagnostico_principal || 'No especificado'}</span></div>
          ${ficha.alergias ? `<div class="emergencia">⚠️ <strong>ALERGIAS:</strong> ${ficha.alergias}</div>` : ''}
          ${ficha.medicamentos_actuales ? `<div class="campo"><strong>Medicamentos actuales:</strong> <span>${ficha.medicamentos_actuales}</span></div>` : ''}
        </div>

        <div class="seccion">
          <h2>📞 Contactos de Emergencia</h2>
          <div class="campo"><strong>Contacto principal:</strong> <span>${ficha.contacto_principal_nombre} (${ficha.contacto_principal_relacion || 'No especificado'})</span></div>
          <div class="campo"><strong>Teléfono principal:</strong> <span style="font-size: 18px; font-weight: bold;">${ficha.contacto_principal_telefono}</span></div>
          ${ficha.contacto_principal_telefono_alt ? `<div class="campo"><strong>Teléfono alternativo:</strong> <span style="font-size: 18px; font-weight: bold;">${ficha.contacto_principal_telefono_alt}</span></div>` : ''}
          ${ficha.contacto_secundario_nombre ? `
            <div class="campo" style="margin-top: 15px;"><strong>Contacto secundario:</strong> <span>${ficha.contacto_secundario_nombre}</span></div>
            <div class="campo"><strong>Teléfono secundario:</strong> <span style="font-size: 18px; font-weight: bold;">${ficha.contacto_secundario_telefono || 'No especificado'}</span></div>
          ` : ''}
        </div>

        ${ficha.seguro_medico || ficha.hospital_preferido || ficha.medico_tratante ? `
        <div class="seccion">
          <h2>🏥 Información Médica Adicional</h2>
          ${ficha.seguro_medico ? `<div class="campo"><strong>Seguro médico:</strong> <span>${ficha.seguro_medico}</span></div>` : ''}
          ${ficha.hospital_preferido ? `<div class="campo"><strong>Hospital preferido:</strong> <span>${ficha.hospital_preferido}</span></div>` : ''}
          ${ficha.medico_tratante ? `<div class="campo"><strong>Médico tratante:</strong> <span>${ficha.medico_tratante}</span></div>` : ''}
        </div>
        ` : ''}

        ${ficha.instrucciones_emergencia || ficha.crisis_comunes || ficha.como_calmar ? `
        <div class="seccion">
          <h2>⚡ Instrucciones de Emergencia</h2>
          ${ficha.instrucciones_emergencia ? `<div class="emergencia">${ficha.instrucciones_emergencia}</div>` : ''}
          ${ficha.crisis_comunes ? `<div class="campo"><strong>Crisis comunes:</strong> <span>${ficha.crisis_comunes}</span></div>` : ''}
          ${ficha.como_calmar ? `<div class="campo"><strong>Cómo calmarlo:</strong> <span>${ficha.como_calmar}</span></div>` : ''}
        </div>
        ` : ''}

        <div class="footer">
          <p>Ficha generada el ${new Date(ficha.fecha_generacion).toLocaleDateString('es-MX', { day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })}</p>
          <p>Centro de Atención de Autismo - Información confidencial</p>
        </div>
      </body>
      </html>
    `;
  }

  obtenerIniciales(nombre: string): string {
    return nombre
      .split(' ')
      .map(n => n[0])
      .join('')
      .substring(0, 2)
      .toUpperCase();
  }
}

