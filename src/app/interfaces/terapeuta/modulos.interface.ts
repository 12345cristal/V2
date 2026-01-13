export interface ModuloTerapeuta {
  id: string;
  nombre: string;
  descripcion: string;
  ruta: string;
  icono: string;
  color: string;
  estado: 'activo' | 'inactivo' | 'en-desarrollo';
  orden: number;
  permisos_requeridos?: string[];
}

export interface ModuloEstado {
  modulo_id: string;
  nombre: string;
  conectado: boolean;
  ultima_actualizacion: string;
  registros_totales: number;
  error?: string;
}

export interface DashboardModulos {
  modulos: ModuloTerapeuta[];
  estados: ModuloEstado[];
  resumen: {
    total_modulos: number;
    modulos_activos: number;
    modulos_inactivos: number;
    modulos_error: number;
  };
}
