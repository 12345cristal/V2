# app/services/google_calendar_service.py
"""
Servicio de integración con Google Calendar usando Service Account
Autor: Backend Senior Developer
Fecha: 16 de diciembre de 2025

IMPORTANTE: Este servicio requiere configuración de Google Cloud Platform
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, date, time, timedelta
from typing import Optional, Dict, Any, List
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class GoogleCalendarService:
    """
    Servicio para gestionar eventos de Google Calendar usando Service Account
    
    CONFIGURACIÓN REQUERIDA:
    1. Crear proyecto en Google Cloud Console
    2. Habilitar Google Calendar API
    3. Crear Service Account y descargar JSON de credenciales
    4. Compartir calendario con el email del Service Account
    5. Configurar variable de entorno GOOGLE_CALENDAR_CREDENTIALS
    """
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self, credentials_path: Optional[str] = None, calendar_id: Optional[str] = None):
        """
        Inicializa el servicio de Google Calendar
        
        Args:
            credentials_path: Ruta al archivo JSON de credenciales
            calendar_id: ID del calendario (por defecto 'primary')
        """
        self.credentials_path = credentials_path or os.getenv(
            'GOOGLE_CALENDAR_CREDENTIALS',
            'credentials/google-calendar-service-account.json'
        )
        self.calendar_id = calendar_id or os.getenv('GOOGLE_CALENDAR_ID', 'primary')
        self.service = None
        self._configurado = False
        
        # Intentar inicializar el servicio
        self._initialize_service()
    
    def _initialize_service(self):
        """Inicializa el servicio de Google Calendar"""
        try:
            # Verificar si existe el archivo de credenciales
            if not os.path.exists(self.credentials_path):
                logger.warning(f"⚠️  Archivo de credenciales no encontrado: {self.credentials_path}")
                logger.info("   Para configurar Google Calendar:")
                logger.info("   1. Crear Service Account en Google Cloud Console")
                logger.info("   2. Habilitar Calendar API")
                logger.info("   3. Descargar JSON de credenciales")
                logger.info(f"   4. Guardar en: {self.credentials_path}")
                return
            
            # Crear credenciales desde el archivo
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )
            
            # Construir el servicio
            self.service = build('calendar', 'v3', credentials=credentials)
            self._configurado = True
            
            logger.info(f"✅ Google Calendar Service configurado correctamente")
            logger.info(f"   Calendario: {self.calendar_id}")
            
        except Exception as e:
            logger.error(f"❌ Error al inicializar Google Calendar Service: {str(e)}")
            self._configurado = False
    
    @property
    def esta_configurado(self) -> bool:
        """Verifica si el servicio está configurado y listo"""
        return self._configurado and self.service is not None
    
    def _combinar_fecha_hora(self, fecha: date, hora: time) -> datetime:
        """Combina fecha y hora en datetime"""
        return datetime.combine(fecha, hora)
    
    def _crear_evento_dict(
        self,
        titulo: str,
        descripcion: str,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        ubicacion: Optional[str] = None,
        recordatorios: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Crea el diccionario de evento para Google Calendar
        
        Args:
            titulo: Título del evento
            descripcion: Descripción detallada
            fecha_inicio: Fecha y hora de inicio
            fecha_fin: Fecha y hora de fin
            ubicacion: Ubicación del evento
            recordatorios: Lista de recordatorios
        
        Returns:
            Diccionario con estructura de evento de Google Calendar
        """
        evento = {
            'summary': titulo,
            'description': descripcion,
            'start': {
                'dateTime': fecha_inicio.isoformat(),
                'timeZone': 'America/Hermosillo',  # Ajustar según tu zona
            },
            'end': {
                'dateTime': fecha_fin.isoformat(),
                'timeZone': 'America/Hermosillo',
            },
            'reminders': {
                'useDefault': False,
                'overrides': recordatorios or [
                    {'method': 'email', 'minutes': 24 * 60},  # 1 día antes
                    {'method': 'popup', 'minutes': 30},  # 30 minutos antes
                ],
            },
        }
        
        if ubicacion:
            evento['location'] = ubicacion
        
        return evento
    
    def crear_evento(
        self,
        titulo: str,
        descripcion: str,
        fecha: date,
        hora_inicio: time,
        hora_fin: time,
        ubicacion: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Optional[Dict[str, str]]:
        """
        Crea un evento en Google Calendar
        
        Args:
            titulo: Título del evento
            descripcion: Descripción
            fecha: Fecha del evento
            hora_inicio: Hora de inicio
            hora_fin: Hora de fin
            ubicacion: Ubicación física
            metadata: Información adicional (niño, terapeuta, etc.)
        
        Returns:
            Dict con google_event_id y google_calendar_link, o None si falla
        """
        if not self.esta_configurado:
            logger.warning("⚠️  Google Calendar no está configurado. Evento NO sincronizado.")
            return None
        
        try:
            # Combinar fecha y hora
            fecha_inicio_dt = self._combinar_fecha_hora(fecha, hora_inicio)
            fecha_fin_dt = self._combinar_fecha_hora(fecha, hora_fin)
            
            # Enriquecer descripción con metadata
            if metadata:
                descripcion += f"\n\n--- Información adicional ---\n"
                for key, value in metadata.items():
                    descripcion += f"{key}: {value}\n"
            
            # Crear evento
            evento = self._crear_evento_dict(
                titulo=titulo,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio_dt,
                fecha_fin=fecha_fin_dt,
                ubicacion=ubicacion
            )
            
            # Insertar en Google Calendar
            evento_creado = self.service.events().insert(
                calendarId=self.calendar_id,
                body=evento
            ).execute()
            
            logger.info(f"✅ Evento creado en Google Calendar: {evento_creado['id']}")
            
            return {
                'google_event_id': evento_creado['id'],
                'google_calendar_link': evento_creado.get('htmlLink', '')
            }
            
        except HttpError as e:
            logger.error(f"❌ Error HTTP al crear evento en Google Calendar: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error al crear evento en Google Calendar: {e}")
            return None
    
    def actualizar_evento(
        self,
        google_event_id: str,
        titulo: Optional[str] = None,
        descripcion: Optional[str] = None,
        fecha: Optional[date] = None,
        hora_inicio: Optional[time] = None,
        hora_fin: Optional[time] = None,
        ubicacion: Optional[str] = None
    ) -> bool:
        """
        Actualiza un evento existente en Google Calendar
        
        Args:
            google_event_id: ID del evento en Google Calendar
            titulo, descripcion, fecha, hora_inicio, hora_fin, ubicacion: Campos a actualizar
        
        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        if not self.esta_configurado:
            logger.warning("⚠️  Google Calendar no está configurado.")
            return False
        
        try:
            # Obtener evento actual
            evento = self.service.events().get(
                calendarId=self.calendar_id,
                eventId=google_event_id
            ).execute()
            
            # Actualizar campos
            if titulo:
                evento['summary'] = titulo
            if descripcion:
                evento['description'] = descripcion
            if ubicacion:
                evento['location'] = ubicacion
            
            if fecha and hora_inicio and hora_fin:
                fecha_inicio_dt = self._combinar_fecha_hora(fecha, hora_inicio)
                fecha_fin_dt = self._combinar_fecha_hora(fecha, hora_fin)
                
                evento['start'] = {
                    'dateTime': fecha_inicio_dt.isoformat(),
                    'timeZone': 'America/Hermosillo',
                }
                evento['end'] = {
                    'dateTime': fecha_fin_dt.isoformat(),
                    'timeZone': 'America/Hermosillo',
                }
            
            # Actualizar en Google Calendar
            self.service.events().update(
                calendarId=self.calendar_id,
                eventId=google_event_id,
                body=evento
            ).execute()
            
            logger.info(f"✅ Evento actualizado en Google Calendar: {google_event_id}")
            return True
            
        except HttpError as e:
            logger.error(f"❌ Error HTTP al actualizar evento: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error al actualizar evento: {e}")
            return False
    
    def eliminar_evento(self, google_event_id: str) -> bool:
        """
        Elimina un evento de Google Calendar
        
        Args:
            google_event_id: ID del evento a eliminar
        
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        if not self.esta_configurado:
            logger.warning("⚠️  Google Calendar no está configurado.")
            return False
        
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=google_event_id
            ).execute()
            
            logger.info(f"✅ Evento eliminado de Google Calendar: {google_event_id}")
            return True
            
        except HttpError as e:
            logger.error(f"❌ Error HTTP al eliminar evento: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error al eliminar evento: {e}")
            return False
    
    def obtener_eventos(
        self,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        max_resultados: int = 100
    ) -> List[Dict]:
        """
        Obtiene eventos del calendario en un rango de fechas
        
        Args:
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango
            max_resultados: Máximo número de resultados
        
        Returns:
            Lista de eventos
        """
        if not self.esta_configurado:
            return []
        
        try:
            # Si no se especifica, obtener eventos del mes actual
            if not fecha_inicio:
                fecha_inicio = datetime.now().replace(day=1, hour=0, minute=0, second=0)
            if not fecha_fin:
                # Último día del mes siguiente
                fecha_fin = fecha_inicio + timedelta(days=60)
            
            eventos = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=fecha_inicio.isoformat() + 'Z',
                timeMax=fecha_fin.isoformat() + 'Z',
                maxResults=max_resultados,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return eventos.get('items', [])
            
        except Exception as e:
            logger.error(f"❌ Error al obtener eventos: {e}")
            return []


# Instancia global del servicio
google_calendar_service = GoogleCalendarService()
