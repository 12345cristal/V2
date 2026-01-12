#!/bin/bash
# 🚀 SCRIPT DE ACTIVACIÓN - MIS HIJOS
# Ejecutar en orden para activar el sistema

echo "╔════════════════════════════════════════════════════╗"
echo "║     🚀 ACTIVACIÓN MÓDULO MIS HIJOS v1.0          ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# PASO 1: Migrar Base de Datos
echo "📊 PASO 1: Migrando base de datos..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Comando: cd backend && python migracion_mis_hijos.py"
echo ""
echo "✅ Esto creará:"
echo "   • Tabla 'medicamentos'"
echo "   • Tabla 'alergias'"
echo "   • Índices para optimización"
echo "   • Datos de prueba (opcional)"
echo ""
read -p "¿Ejecutar migración? (s/n): " migrate
if [ "$migrate" = "s" ]; then
    cd backend
    python migracion_mis_hijos.py
    cd ..
    echo "✅ Migración completada"
else
    echo "⏭️  Saltando migración"
fi
echo ""

# PASO 2: Backend
echo "🔧 PASO 2: Iniciando backend..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Comando: cd backend && python run_server.py"
echo ""
echo "✅ Espera a que veas:"
echo "   ✓ Uvicorn running on http://127.0.0.1:8000"
echo "   ✓ Application startup complete"
echo ""
read -p "¿Iniciar backend en otra terminal? (s/n): " backend_start
if [ "$backend_start" = "s" ]; then
    echo "⚠️  Abre otra terminal y ejecuta:"
    echo "   cd backend && python run_server.py"
    read -p "Presiona Enter cuando esté el backend listo..."
fi
echo ""

# PASO 3: Frontend
echo "🎨 PASO 3: Compilando frontend..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Comando: ng serve"
echo ""
echo "✅ Espera a que veas:"
echo "   ✓ Compiled successfully"
echo "   ✓ Application bundle generation complete"
echo ""
ng serve &
echo ""

# PASO 4: Acceso
echo "🌐 PASO 4: Acceso a la aplicación"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "URL: http://localhost:4200/padre/mis-hijos"
echo ""
echo "✅ Pasos para acceder:"
echo "   1. Abre http://localhost:4200"
echo "   2. Login con usuario padre"
echo "   3. Navega a /padre/mis-hijos"
echo ""

echo "╔════════════════════════════════════════════════════╗"
echo "║          ✅ SISTEMA LISTO PARA USAR               ║"
echo "║                                                    ║"
echo "║   Frontend: http://localhost:4200                 ║"
echo "║   Backend:  http://localhost:8000/docs            ║"
echo "║   BD:       MySQL - Verificar phpMyAdmin          ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "📞 Soporte:"
echo "   • Frontend issues: Revisar SOLUCION_ERRORES_ANGULAR.md"
echo "   • Backend issues: Revisar BACKEND_MIS_HIJOS_GUIA.md"
echo "   • General: Ver RESUMEN_FINAL_MIS_HIJOS.md"
echo ""
