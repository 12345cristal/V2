# app/core/database.py
"""
Módulo de base de datos - Re-exporta funciones de app.db.session
para mantener compatibilidad con imports existentes.
"""
from app.db.session import engine, SessionLocal, get_db

__all__ = ["engine", "SessionLocal", "get_db"]
