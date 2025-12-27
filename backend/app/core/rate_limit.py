"""
Rate Limiting Simple por IP
Sin dependencias externas - producción ready
"""
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
import threading

class SimpleRateLimiter:
    """
    Rate limiter en memoria por IP
    Thread-safe y auto-limpiante
    """
    def __init__(self, max_requests: int = 20, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # IP -> (contador, timestamp_ventana)
        self.requests: Dict[str, Tuple[int, datetime]] = defaultdict(lambda: (0, datetime.now()))
        self.lock = threading.Lock()
    
    def _get_client_ip(self, request: Request) -> str:
        """Extrae IP del cliente (considera proxies)"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
    
    def _cleanup_old_entries(self):
        """Limpia entradas antiguas (llamar periódicamente)"""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window_seconds * 2)
        
        with self.lock:
            to_delete = [
                ip for ip, (_, timestamp) in self.requests.items()
                if timestamp < cutoff
            ]
            for ip in to_delete:
                del self.requests[ip]
    
    def check_rate_limit(self, request: Request) -> None:
        """
        Verifica rate limit - lanza HTTPException si se excede
        """
        ip = self._get_client_ip(request)
        now = datetime.now()
        
        with self.lock:
            count, window_start = self.requests[ip]
            
            # Si la ventana expiró, reiniciar
            if now - window_start > timedelta(seconds=self.window_seconds):
                self.requests[ip] = (1, now)
                return
            
            # Si estamos dentro de la ventana, incrementar
            if count >= self.max_requests:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit excedido",
                        "mensaje": f"Máximo {self.max_requests} solicitudes por {self.window_seconds}s",
                        "retry_after": self.window_seconds
                    }
                )
            
            self.requests[ip] = (count + 1, window_start)
        
        # Limpiar ocasionalmente (1% de probabilidad)
        if hash(ip) % 100 == 0:
            self._cleanup_old_entries()

# Instancia global para chatbot
# 20 requests por minuto por IP
chatbot_limiter = SimpleRateLimiter(max_requests=20, window_seconds=60)
