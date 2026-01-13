// src/app/coordinador/asignar-terapias/asignar-terapias.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CitasCalendarioService, CitaCalendarioCreate } from '../../service/citas-calendario.service';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { forkJoin } from 'rxjs';

interface Nino {
  id: number;
  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string;
}

interface Terapeuta {
  id: number;
  nombres: string;
  apellido_paterno: string;
  apellido_materno?: string;
  especialidad?: string;
  terapia_id?: number; // ID de la terapia que realiza
}

interface Terapia {
  id: number;
  nombre: string;
  duracion_minutos: number;
  descripcion?: string;
}

interface AsignacionTerapia {
  nino: Nino | null;
  terapeuta: Terapeuta | null;
  terapia: Terapia | null;
  fechaInicio: string;
  diasSemana: number[]; // 1=Lunes, 2=Martes, etc.
  horaInicio: string;
  horaFin: string;
  cantidadSemanas: number;
  sincronizarGoogle: boolean;
}

@Component({
  selector: 'app-asignar-terapias',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './asignar-terapias.component.html',
  styleUrls: ['./asignar-terapias.component.scss']
})
export class AsignarTerapiasComponent implements OnInit {
  
  // Catálogos
  ninos: Nino[] = [];
  terapeutas: Terapeuta[] = [];
  // Para el modal: lista de terapeutas filtrados por terapia
  get terapeutasFiltradosLista(): Terapeuta[] {
    if (!this.formularioEvento.terapiaId) return this.terapeutas;
    // Si hubiese mapeo real, filtrar por especialidad/terapia
    return this.terapeutas;
  }
  terapias: Terapia[] = [];
  
  // Estado de carga
  cargando = false;
  cargandoNinos = false;
  cargandoTerapeutas = false;
  cargandoTerapias = false;
  
  // Asignación actual (legacy - no usada en vista calendario pero mantenida)
  asignacion: AsignacionTerapia = {
    nino: null,
    terapeuta: null,
    terapia: null,
    fechaInicio: this.obtenerFechaManana(),
    diasSemana: [],
    horaInicio: '09:00',
    horaFin: '10:00',
    cantidadSemanas: 4,
    sincronizarGoogle: true
  };
  
  // Opciones de días
  opcionesDias = [
    { valor: 1, nombre: 'Lunes', seleccionado: false },
    { valor: 2, nombre: 'Martes', seleccionado: false },
    { valor: 3, nombre: 'Miércoles', seleccionado: false },
    { valor: 4, nombre: 'Jueves', seleccionado: false },
    { valor: 5, nombre: 'Viernes', seleccionado: false },
    { valor: 6, nombre: 'Sábado', seleccionado: false }
  ];
  
  // Horas predefinidas (legacy)
  horasPredefinidas = [
    '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
    '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'
  ];
  
  // Mensajes
  mensajeExito = '';
  mensajeError = '';
  
  // Previsualización (legacy)
  citasGeneradas: any[] = [];
  mostrarPrevisualizacion = false;

  // ================= CALENDARIO =================
  vistaActual: 'semana' | 'dia' | 'mes' = 'semana';
  sidebarAbierto = true;
  fechaReferencia: Date = new Date();
  diasSemanaCortos = ['L', 'M', 'X', 'J', 'V', 'S', 'D'];
  diasSemana: Array<{ fecha: string; nombre: string; numero: number; esHoy: boolean }> = [];
  horasDelDia: string[] = [];
  eventos: Array<{
    id: number;
    fecha: string; // YYYY-MM-DD
    horaInicio: string; // HH:MM
    horaFin: string; // HH:MM
    ninoId: number;
    terapeutaId: number;
    terapiaId: number;
    ninoNombre: string;
    terapeutaNombre: string;
    terapiaNombre: string;
    estadoId: number;
    estado: 'programada' | 'reprogramada' | 'cancelada' | 'otro';
    googleCalendarLink?: string;
    sincronizadoGoogle?: boolean;
  }> = [];
  eventoDragging: any = null;

  // Mini calendario
  diasMiniCalendario: Array<{ fecha: Date; numero: number; mesActual: boolean; esHoy: boolean; seleccionado: boolean }> = [];
  mesMiniActual: Date = new Date();

  // Filtros
  filtroNino = '';
  filtroNinoId: number | null = null;
  filtroTerapeutaId: number | null = null;
  filtroTerapiaId: number | null = null;
  verTodo = false;
  ninosFiltrados: number[] = [];
  terapeutasFiltrados: number[] = [];
  terapiasFiltradas: number[] = [];
  mostrarProgramadas = true;
  mostrarReprogramadas = true;
  mostrarCanceladas = true;

  // Estados de cita (mapas)
  estadoCodigoPorId: Record<number, string> = {};
  estadoIdPorCodigo: Record<string, number> = {};

  // Modal
  modalAbierto = false;
  eventoEditando: any = null;
  formularioEvento: {
    ninoId: number | null;
    terapeutaId: number | null;
    terapiaId: number | null;
    fecha: string; // YYYY-MM-DD
    horaInicio: string; // HH:MM
    horaFin: string; // HH:MM
    esRecurrente: boolean;
    cantidadSemanas: number;
    observaciones?: string;
    sincronizarGoogle: boolean;
  } = {
    ninoId: null,
    terapeutaId: null,
    terapiaId: null,
    fecha: this.formatearFecha(new Date()),
    horaInicio: '09:00',
    horaFin: '10:00',
    esRecurrente: false,
    cantidadSemanas: 4,
    observaciones: '',
    sincronizarGoogle: true
  };
  
  constructor(
    private citasCalendarioService: CitasCalendarioService,
    private http: HttpClient
  ) {}
  
  ngOnInit(): void {
    this.cargarCatalogos();
    this.cargarEstados();
    this.generarSemana();
    this.generarHorasDia();
    this.generarMiniCalendario();
    this.cargarEventosSemana();
  }
  
  // ============================================================
  // CARGA DE CATÁLOGOS
  // ============================================================
  
  cargarCatalogos(): void {
    this.cargarNinos();
    this.cargarTerapeutas();
    this.cargarTerapias();
  }
  
  cargarNinos(): void {
    this.cargandoNinos = true;
    this.http.get<any>(`${environment.apiBaseUrl}/ninos`).subscribe({
      next: (response) => {
        this.ninos = response.items || response;
        this.cargandoNinos = false;
      },
      error: (error) => {
        console.error('Error al cargar niños:', error);
        this.cargandoNinos = false;
      }
    });
  }
  
  cargarTerapeutas(): void {
    this.cargandoTerapeutas = true;
    this.http.get<any>(`${environment.apiBaseUrl}/personal`).subscribe({
      next: (response) => {
        this.terapeutas = response.items || response;
        this.cargandoTerapeutas = false;
      },
      error: (error) => {
        console.error('Error al cargar terapeutas:', error);
        this.cargandoTerapeutas = false;
      }
    });
  }
  
  cargarTerapias(): void {
    this.cargandoTerapias = true;
    this.http.get<any>(`${environment.apiBaseUrl}/terapias`).subscribe({
      next: (response) => {
        this.terapias = response.items || response;
        this.cargandoTerapias = false;
      },
      error: (error) => {
        console.error('Error al cargar terapias:', error);
        this.cargandoTerapias = false;
      }
    });
  }

  // Estados de cita
  cargarEstados(): void {
    this.citasCalendarioService.obtenerEstadosCita().subscribe({
      next: (estados) => {
        estados.forEach(e => {
          const codigo = (e.codigo || e.nombre || '').toString().toLowerCase();
          this.estadoCodigoPorId[e.id] = codigo;
          this.estadoIdPorCodigo[codigo] = e.id;
        });
      },
      error: (err) => console.warn('No se pudieron cargar estados de cita', err)
    });
  }
  
  // ============================================================
  // SELECCIÓN DE DATOS
  // ============================================================
  
  onNinoChange(nino: Nino): void {
    this.asignacion.nino = nino;
  }
  
  onTerapeutaChange(terapeuta: Terapeuta): void {
    this.asignacion.terapeuta = terapeuta;
  }
  
  onTerapiaChange(terapia: Terapia): void {
    this.asignacion.terapia = terapia;
    this.asignacion.terapeuta = null; // Reset terapeuta al cambiar terapia
    
    // Filtrar terapeutas que pueden realizar esta terapia
    if (terapia) {
      this.filtrarTerapeutasPorTerapia(terapia.id);
      
      // Ajustar hora fin según duración de la terapia
      if (terapia.duracion_minutos) {
        this.ajustarHoraFin(terapia.duracion_minutos);
      }
    } else {
      this.terapeutasFiltrados = [];
    }
  }
  
  filtrarTerapeutasPorTerapia(terapiaId: number): void {
    // En la vista actual el modal usa `terapeutasFiltradosLista` (getter)
    // que calcula dinámicamente la lista de terapeutas a mostrar.
    // Aquí no es necesario modificar `terapeutasFiltrados` (ids de filtro global).
  }
  
  onDiaChange(dia: any): void {
    dia.seleccionado = !dia.seleccionado;
    this.asignacion.diasSemana = this.opcionesDias
      .filter(d => d.seleccionado)
      .map(d => d.valor);
  }
  
  ajustarHoraFin(duracionMinutos: number): void {
    const [horas, minutos] = this.asignacion.horaInicio.split(':').map(Number);
    const totalMinutos = horas * 60 + minutos + duracionMinutos;
    const nuevasHoras = Math.floor(totalMinutos / 60);
    const nuevosMinutos = totalMinutos % 60;
    
    this.asignacion.horaFin = `${String(nuevasHoras).padStart(2, '0')}:${String(nuevosMinutos).padStart(2, '0')}`;
  }

  // ================== CALENDARIO: SEMANA/HORAS ==================
  private inicioSemana(fecha: Date): Date {
    const f = new Date(fecha);
    const dia = f.getDay(); // 0=Dom,1=Lun
    const offset = dia === 0 ? -6 : 1 - dia; // Lunes
    f.setDate(f.getDate() + offset);
    f.setHours(0, 0, 0, 0);
    return f;
  }

  formatearFecha(fecha: Date): string {
    const y = fecha.getFullYear();
    const m = String(fecha.getMonth() + 1).padStart(2, '0');
    const d = String(fecha.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
  }

  generarSemana(): void {
    const inicio = this.inicioSemana(this.fechaReferencia);
    const hoyStr = this.formatearFecha(new Date());
    this.diasSemana = Array.from({ length: 6 }).map((_, i) => {
      const fecha = new Date(inicio);
      fecha.setDate(inicio.getDate() + i);
      const fechaStr = this.formatearFecha(fecha);
      const nombres = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'];
      return {
        fecha: fechaStr,
        nombre: nombres[i],
        numero: fecha.getDate(),
        esHoy: fechaStr === hoyStr
      };
    });
  }

  generarHorasDia(): void {
    const horas: string[] = [];
    for (let h = 8; h <= 18; h++) {
      horas.push(`${String(h).padStart(2, '0')}:00`);
    }
    this.horasDelDia = horas;
  }

  obtenerTituloPeriodo(): string {
    if (!this.diasSemana.length) return '';
    const inicio = this.diasSemana[0];
    const fin = this.diasSemana[this.diasSemana.length - 1];
    const fIni = new Date(inicio.fecha);
    const fFin = new Date(fin.fecha);
    const meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
    if (fIni.getMonth() === fFin.getMonth()) {
      return `${fIni.getDate()}–${fFin.getDate()} de ${meses[fIni.getMonth()]} ${fIni.getFullYear()}`;
    }
    return `${fIni.getDate()} ${meses[fIni.getMonth()]} – ${fFin.getDate()} ${meses[fFin.getMonth()]} ${fFin.getFullYear()}`;
  }

  irHoy(): void {
    this.fechaReferencia = new Date();
    this.generarSemana();
    this.generarMiniCalendario();
    this.cargarEventosSemana();
  }

  semanaSiguiente(delta: number): void {
    const f = new Date(this.fechaReferencia);
    f.setDate(f.getDate() + (7 * delta));
    this.fechaReferencia = f;
    this.generarSemana();
    this.generarMiniCalendario();
    this.cargarEventosSemana();
  }

  cambiarVista(v: 'semana' | 'dia' | 'mes'): void {
    this.vistaActual = v;
  }

  toggleSidebar(): void {
    this.sidebarAbierto = !this.sidebarAbierto;
  }

  // ================== MINI CALENDARIO ==================
  generarMiniCalendario(): void {
    const base = new Date(this.fechaReferencia);
    this.mesMiniActual = new Date(base.getFullYear(), base.getMonth(), 1);
    const inicioMes = new Date(this.mesMiniActual);
    const inicioSemanaMes = this.inicioSemana(inicioMes);
    const dias: Array<{ fecha: Date; numero: number; mesActual: boolean; esHoy: boolean; seleccionado: boolean }> = [];
    const hoy = this.formatearFecha(new Date());

    for (let i = 0; i < 42; i++) { // 6 filas
      const d = new Date(inicioSemanaMes);
      d.setDate(inicioSemanaMes.getDate() + i);
      const esMesActual = d.getMonth() === this.mesMiniActual.getMonth();
      const esHoy = this.formatearFecha(d) === hoy;
      const seleccionado = this.diasSemana.some(x => x.fecha === this.formatearFecha(d));
      dias.push({ fecha: d, numero: d.getDate(), mesActual: esMesActual, esHoy, seleccionado });
    }
    this.diasMiniCalendario = dias;
  }

  obtenerMesMini(): string {
    const meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
    return `${meses[this.mesMiniActual.getMonth()]} ${this.mesMiniActual.getFullYear()}`;
  }

  cambiarMesMini(delta: number): void {
    const m = new Date(this.mesMiniActual);
    m.setMonth(m.getMonth() + delta);
    this.mesMiniActual = m;
    this.generarMiniCalendario();
  }

  cambiarAnioMini(delta: number): void {
    const m = new Date(this.mesMiniActual);
    m.setFullYear(m.getFullYear() + delta);
    this.mesMiniActual = m;
    this.generarMiniCalendario();
  }

  seleccionarDiaMini(dia: { fecha: Date }): void {
    this.fechaReferencia = new Date(dia.fecha);
    this.generarSemana();
    this.generarMiniCalendario();
    this.cargarEventosSemana();
  }

  abrirSelectorFecha(): void {
    // Placeholder para futuro modal de selección de fecha
    // Por ahora no hace nada, pero el click está preparado
  }

  // ================== CARGA DE EVENTOS ==================
  cargarEventosSemana(): void {
    if (!this.diasSemana.length) return;
    if (!this.verTodo && !this.filtroNinoId && !this.filtroTerapeutaId && !this.filtroTerapiaId) {
      this.eventos = [];
      return;
    }
    this.cargando = true;
    const requests = this.diasSemana.map(d => this.citasCalendarioService.listarPorFecha(d.fecha, {
      nino_id: this.filtroNinoId || undefined,
      terapeuta_id: this.filtroTerapeutaId || undefined,
      terapia_id: this.filtroTerapiaId || undefined
    }));
    forkJoin(requests).subscribe({
      next: (respuestas) => {
        const todos = respuestas.flatMap(r => (r?.items ?? []));
        this.eventos = todos.map(c => {
          const estadoCod = (c.estado_nombre || this.estadoCodigoPorId[c.estado_id] || 'programada').toString().toLowerCase();
          return {
            id: c.id_cita,
            fecha: c.fecha,
            horaInicio: (c.hora_inicio || '').slice(0,5),
            horaFin: (c.hora_fin || '').slice(0,5),
            ninoId: c.nino_id,
            terapeutaId: c.terapeuta_id,
            terapiaId: c.terapia_id,
            ninoNombre: c.nino_nombre || this.buscarNombrePorId(this.ninos, c.nino_id),
            terapeutaNombre: c.terapeuta_nombre || this.buscarNombrePorId(this.terapeutas, c.terapeuta_id),
            terapiaNombre: c.terapia_nombre || (this.terapias.find(t => t.id === c.terapia_id)?.nombre || 'Terapia'),
            estadoId: c.estado_id,
            estado: (estadoCod as any),
            googleCalendarLink: (c as any).google_calendar_link,
            sincronizadoGoogle: (c as any).sincronizado_calendar
          };
        });
        this.cargando = false;
      },
      error: (err) => {
        console.error('Error al cargar eventos semana', err);
        this.cargando = false;
      }
    });
  }

  private buscarNombrePorId(lista: any[], id: number): string {
    const p = lista.find(x => x.id === id);
    return p ? this.obtenerNombreCompleto(p) : '';
  }

  obtenerEventosDia(fecha: string) {
    return this.eventos.filter(e => {
      if (e.fecha !== fecha) return false;
      if (this.ninosFiltrados.length && !this.ninosFiltrados.includes(e.ninoId)) return false;
      if (this.terapeutasFiltrados.length && !this.terapeutasFiltrados.includes(e.terapeutaId)) return false;
      if (this.terapiasFiltradas.length && !this.terapiasFiltradas.includes(e.terapiaId)) return false;
      if (!this.mostrarProgramadas && e.estado === 'programada') return false;
      if (!this.mostrarReprogramadas && e.estado === 'reprogramada') return false;
      if (!this.mostrarCanceladas && e.estado === 'cancelada') return false;
      return true;
    });
  }

  // ================== DRAG & DROP / RESIZE (básico) ==================
  onDragStart(ev: DragEvent, evento: any): void {
    this.eventoDragging = evento;
    ev.dataTransfer?.setData('text/plain', JSON.stringify({ id: evento.id }));
  }
  onDragOver(ev: DragEvent): void { ev.preventDefault(); }
  onDragEnd(_ev: DragEvent): void { this.eventoDragging = null; }
  onDrop(ev: DragEvent, dia: { fecha: string }): void {
    ev.preventDefault();
    if (!this.eventoDragging) return;
    const evento = this.eventoDragging;
    if (evento.fecha === dia.fecha) return; // mismo día
    // Actualizar fecha conservando horas
    this.actualizarCita(evento.id, {
      fecha: dia.fecha,
      hora_inicio: `${evento.horaInicio}:00`,
      hora_fin: `${evento.horaFin}:00`,
      nino_id: evento.ninoId,
      terapeuta_id: evento.terapeutaId,
      terapia_id: evento.terapiaId
    });
  }
  onResizeStart(_ev: MouseEvent, _evento: any): void { /* Placeholder para futuro */ }

  calcularPosicionTop(hora: string): number {
    const [h, m] = hora.split(':').map(Number);
    const inicio = 8; // 08:00
    const minutosDesdeInicio = (h - inicio) * 60 + m;
    const pxPorMinuto = 1; // 60px por hora
    return Math.max(0, minutosDesdeInicio * pxPorMinuto);
  }

  calcularAltura(inicio: string, fin: string): number {
    const [h1, m1] = inicio.split(':').map(Number);
    const [h2, m2] = fin.split(':').map(Number);
    const mins = (h2 * 60 + m2) - (h1 * 60 + m1);
    return Math.max(30, mins * 1);
  }

  abrirEnGoogle(evento: any): void {
    if (evento.googleCalendarLink) {
      window.open(evento.googleCalendarLink, '_blank');
    } else {
      this.mensajeError = 'Este evento aún no tiene enlace de Google Calendar';
    }
  }

  // ================== MODAL ==================
  abrirModalNuevaTerapia(): void {
    const fechaDefault = this.diasSemana.length ? this.diasSemana[0].fecha : this.formatearFecha(new Date());
    this.eventoEditando = null;
    this.formularioEvento = {
      ninoId: null,
      terapeutaId: null,
      terapiaId: null,
      fecha: fechaDefault,
      horaInicio: '09:00',
      horaFin: '10:00',
      esRecurrente: false,
      cantidadSemanas: 4,
      observaciones: '',
      sincronizarGoogle: true
    };
    this.modalAbierto = true;
  }

  abrirModalEditar(evento: any): void {
    this.eventoEditando = evento;
    this.formularioEvento = {
      ninoId: evento.ninoId,
      terapeutaId: evento.terapeutaId,
      terapiaId: evento.terapiaId,
      fecha: evento.fecha,
      horaInicio: evento.horaInicio,
      horaFin: evento.horaFin,
      esRecurrente: false,
      cantidadSemanas: 1,
      observaciones: '',
      sincronizarGoogle: true
    };
    this.modalAbierto = true;
  }

  cerrarModal(): void { this.modalAbierto = false; }

  formularioValido(): boolean {
    const f = this.formularioEvento;
    return !!(f.ninoId && f.terapiaId && f.terapeutaId && f.fecha && f.horaInicio < f.horaFin);
  }

  onTerapiaChangeModal(terapiaId: number | null): void {
    if (!terapiaId) return;
    const t = this.terapias.find(x => x.id === terapiaId);
    if (t && this.formularioEvento.horaInicio) {
      const [h, m] = this.formularioEvento.horaInicio.split(':').map(Number);
      const total = h * 60 + m + (t.duracion_minutos || 60);
      const nh = Math.floor(total / 60), nm = total % 60;
      this.formularioEvento.horaFin = `${String(nh).padStart(2,'0')}:${String(nm).padStart(2,'0')}`;
    }
  }

  guardarEvento(): void {
    if (!this.formularioValido()) return;
    this.cargando = true;
    this.mensajeError = '';
    const f = this.formularioEvento;

    if (this.eventoEditando) {
      this.actualizarCita(this.eventoEditando.id, {
        nino_id: f.ninoId!,
        terapeuta_id: f.terapeutaId!,
        terapia_id: f.terapiaId!,
        fecha: f.fecha,
        hora_inicio: `${f.horaInicio}:00`,
        hora_fin: `${f.horaFin}:00`,
        observaciones: f.observaciones
      });
    } else {
      // Crear una o múltiples
      let asignaciones: CitaCalendarioCreate[] = [];
      if (f.esRecurrente) {
        const diasSeleccionados = this.opcionesDias.filter(d => d.seleccionado).map(d => d.valor);
        const fechas = this.citasCalendarioService.generarFechasRecurrentes(new Date(f.fecha), f.cantidadSemanas, diasSeleccionados, f.horaInicio, f.horaFin);
        asignaciones = fechas.map(fe => ({
          nino_id: f.ninoId!,
          terapeuta_id: f.terapeutaId!,
          terapia_id: f.terapiaId!,
          fecha: fe.fecha,
          hora_inicio: `${fe.hora_inicio}:00`.slice(0,8),
          hora_fin: `${fe.hora_fin}:00`.slice(0,8),
          estado_id: this.estadoIdPorCodigo['programada'] || 1,
          motivo: `Sesión de terapia`,
          observaciones: f.observaciones,
          sincronizar_google_calendar: f.sincronizarGoogle
        }));
      } else {
        asignaciones = [{
          nino_id: f.ninoId!,
          terapeuta_id: f.terapeutaId!,
          terapia_id: f.terapiaId!,
          fecha: f.fecha,
          hora_inicio: `${f.horaInicio}:00`,
          hora_fin: `${f.horaFin}:00`,
          estado_id: this.estadoIdPorCodigo['programada'] || 1,
          motivo: `Sesión de terapia`,
          observaciones: f.observaciones,
          sincronizar_google_calendar: f.sincronizarGoogle
        }];
      }

      this.crearCitasSecuencial(asignaciones, 0, 0, 0);
    }
  }

  private actualizarCita(id: number, data: Partial<CitaCalendarioCreate>): void {
    this.citasCalendarioService.actualizarCita(id, data).subscribe({
      next: () => {
        this.cargando = false;
        this.mensajeExito = 'Cambios guardados';
        this.modalAbierto = false;
        this.cargarEventosSemana();
      },
      error: (err) => {
        this.cargando = false;
        this.mensajeError = 'No se pudo actualizar la cita';
        console.error(err);
      }
    });
  }

  cancelarTerapia(): void {
    if (!this.eventoEditando) return;
    const idCancelada = this.estadoIdPorCodigo['cancelada'] || 3;
    this.cargando = true;
    this.citasCalendarioService.cambiarEstado(this.eventoEditando.id, idCancelada).subscribe({
      next: () => {
        this.cargando = false;
        this.mensajeExito = 'Terapia cancelada';
        this.modalAbierto = false;
        this.cargarEventosSemana();
      },
      error: (err) => {
        this.cargando = false;
        this.mensajeError = 'No se pudo cancelar la terapia';
        console.error(err);
      }
    });
  }
  
  // ============================================================
  // PREVISUALIZACIÓN
  // ============================================================
  
  previsualizarCitas(): void {
    if (!this.validarAsignacion()) {
      return;
    }
    
    const fechaInicio = new Date(this.asignacion.fechaInicio);
    this.citasGeneradas = this.citasCalendarioService.generarFechasRecurrentes(
      fechaInicio,
      this.asignacion.cantidadSemanas,
      this.asignacion.diasSemana,
      this.asignacion.horaInicio,
      this.asignacion.horaFin
    );
    
    this.mostrarPrevisualizacion = true;
  }
  
  cerrarPrevisualizacion(): void {
    this.mostrarPrevisualizacion = false;
  }
  
  // ============================================================
  // ASIGNACIÓN DE TERAPIAS
  // ============================================================
  
  asignarTerapias(): void {
    if (!this.validarAsignacion()) {
      return;
    }
    
    this.cargando = true;
    this.mensajeExito = '';
    this.mensajeError = '';
    
    // Generar fechas
    const fechaInicio = new Date(this.asignacion.fechaInicio);
    const fechas = this.citasCalendarioService.generarFechasRecurrentes(
      fechaInicio,
      this.asignacion.cantidadSemanas,
      this.asignacion.diasSemana,
      this.asignacion.horaInicio,
      this.asignacion.horaFin
    );
    
    // Crear citas
    const citas: CitaCalendarioCreate[] = fechas.map(f => ({
      nino_id: this.asignacion.nino!.id,
      terapeuta_id: this.asignacion.terapeuta!.id,
      terapia_id: this.asignacion.terapia!.id,
      fecha: f.fecha,
      hora_inicio: f.hora_inicio,
      hora_fin: f.hora_fin,
      estado_id: 1, // PROGRAMADA
      motivo: `Sesión de ${this.asignacion.terapia!.nombre}`,
      sincronizar_google_calendar: this.asignacion.sincronizarGoogle
    }));
    
    // Crear todas las citas
    let citasCreadas = 0;
    let citasError = 0;
    
    this.crearCitasSecuencial(citas, 0, citasCreadas, citasError);
  }
  
  private crearCitasSecuencial(
    citas: CitaCalendarioCreate[],
    indice: number,
    creadas: number,
    errores: number
  ): void {
    if (indice >= citas.length) {
      // Terminó de crear todas las citas
      this.cargando = false;
      
      if (creadas > 0) {
        this.mensajeExito = `✅ Se crearon ${creadas} citas exitosamente`;
        if (this.asignacion.sincronizarGoogle) {
          this.mensajeExito += ' y se sincronizaron con Google Calendar';
        }
        this.modalAbierto = false;
        this.cargarEventosSemana();
      }
      
      if (errores > 0) {
        this.mensajeError = `⚠️ ${errores} citas no pudieron crearse`;
      }
      
      return;
    }
    
    // Crear cita actual
    this.citasCalendarioService.crearCita(citas[indice]).subscribe({
      next: () => {
        this.crearCitasSecuencial(citas, indice + 1, creadas + 1, errores);
      },
      error: (error) => {
        console.error('Error al crear cita:', error);
        this.crearCitasSecuencial(citas, indice + 1, creadas, errores + 1);
      }
    });
  }
  
  // ============================================================
  // VALIDACIÓN
  // ============================================================
  
  validarAsignacion(): boolean {
    if (!this.asignacion.nino) {
      this.mensajeError = 'Debe seleccionar un niño';
      return false;
    }
    
    if (!this.asignacion.terapeuta) {
      this.mensajeError = 'Debe seleccionar un terapeuta';
      return false;
    }
    
    if (!this.asignacion.terapia) {
      this.mensajeError = 'Debe seleccionar una terapia';
      return false;
    }
    
    if (this.asignacion.diasSemana.length === 0) {
      this.mensajeError = 'Debe seleccionar al menos un día de la semana';
      return false;
    }
    
    if (!this.asignacion.fechaInicio) {
      this.mensajeError = 'Debe seleccionar una fecha de inicio';
      return false;
    }
    
    if (this.asignacion.horaInicio >= this.asignacion.horaFin) {
      this.mensajeError = 'La hora de inicio debe ser anterior a la hora de fin';
      return false;
    }
    
    this.mensajeError = '';
    return true;
  }
  
  // ============================================================
  // UTILIDADES
  // ============================================================
  
  obtenerFechaManana(): string {
    const manana = new Date();
    manana.setDate(manana.getDate() + 1);
    return manana.toISOString().split('T')[0];
  }
  
  limpiarFormulario(): void {
    this.asignacion = {
      nino: null,
      terapeuta: null,
      terapia: null,
      fechaInicio: this.obtenerFechaManana(),
      diasSemana: [],
      horaInicio: '09:00',
      horaFin: '10:00',
      cantidadSemanas: 4,
      sincronizarGoogle: true
    };
    
    this.opcionesDias.forEach(dia => dia.seleccionado = false);
    this.mostrarPrevisualizacion = false;
    this.citasGeneradas = [];
  }
  
  obtenerNombreCompleto(persona: any): string {
    if (!persona) return '';
    const nombres = persona.nombres || '';
    const paterno = persona.apellido_paterno || '';
    const materno = persona.apellido_materno || '';
    return `${nombres} ${paterno} ${materno}`.trim() || 'Sin nombre';
  }
  
  obtenerDiaNombre(numeroD: number): string {
    const dia = this.opcionesDias.find(d => d.valor === numeroD);
    return dia ? dia.nombre : '';
  }

  // ================== FILTROS ==================
  toggleFiltroNino(id: number): void {
    this.toggleId(this.ninosFiltrados, id);
  }
  toggleFiltroTerapeuta(id: number): void {
    this.toggleId(this.terapeutasFiltrados, id);
  }
  toggleFiltroTerapia(id: number): void {
    this.toggleId(this.terapiasFiltradas, id);
  }
  limpiarFiltros(): void {
    this.filtroNino = '';
    this.filtroNinoId = null;
    this.filtroTerapeutaId = null;
    this.filtroTerapiaId = null;
    this.ninosFiltrados = [];
    this.terapeutasFiltrados = [];
    this.terapiasFiltradas = [];
    this.mostrarProgramadas = this.mostrarReprogramadas = this.mostrarCanceladas = true;
    this.verTodo = false;
  }
  private toggleId(arr: number[], id: number) {
    const idx = arr.indexOf(id);
    if (idx >= 0) arr.splice(idx, 1); else arr.push(id);
  }

  aplicarFiltros(): void {
    this.ninosFiltrados = this.filtroNinoId ? [this.filtroNinoId] : [];
    this.terapeutasFiltrados = this.filtroTerapeutaId ? [this.filtroTerapeutaId] : [];
    this.terapiasFiltradas = this.filtroTerapiaId ? [this.filtroTerapiaId] : [];
    this.cargarEventosSemana();
  }

  // 🔑 TrackBy functions para @for loops (evita NG0955)
  trackByIndex(index: number): number {
    return index;
  }

  trackByDia(index: number, dia: string | any): string | number {
    // Si es un string simple, retornarlo
    if (typeof dia === 'string') {
      return dia;
    }
    // Si es un objeto con fecha, usar la fecha
    if (dia && dia.fecha) {
      return typeof dia.fecha === 'string' ? dia.fecha : dia.fecha.toISOString();
    }
    // Si es un objeto con nombre, usar el nombre
    if (dia && dia.nombre) {
      return dia.nombre;
    }
    // Fallback: usar índice
    return index;
  }

  trackByHora(index: number, hora: string): string {
    return hora;
  }

  trackByNino(index: number, nino: Nino): number {
    return nino?.id ?? index;
  }

  trackByTerapeuta(index: number, terapeuta: Terapeuta): number {
    return terapeuta?.id ?? index;
  }

  trackByTerapia(index: number, terapia: Terapia): number {
    return terapia?.id ?? index;
  }
}



