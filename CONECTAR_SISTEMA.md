# 🚀 GUÍA RÁPIDA: CONECTAR BACKEND CON FRONTEND

## ❌ Problema Actual
El frontend no puede conectarse al backend porque:
1. El backend no está corriendo (puerto 8000)
2. La base de datos no existe

## ✅ Solución en 3 Pasos

### PASO 1: Crear la Base de Datos

#### Opción A: phpMyAdmin (RECOMENDADO - 30 segundos)

1. **Abre XAMPP Control Panel**
2. **Inicia MySQL** (botón "Start" al lado de MySQL)
3. **Abre phpMyAdmin**: http://localhost/phpmyadmin
4. **Click en "SQL"** (pestaña arriba)
5. **Copia y pega esto:**
   ```sql
   CREATE DATABASE IF NOT EXISTS autismo_mochis_ia 
   CHARACTER SET utf8mb4 
   COLLATE utf8mb4_general_ci;
   ```
6. **Click "Continuar"**

✅ ¡Listo! Base de datos creada.

---

### PASO 2: Iniciar el Backend

Abre una **nueva terminal PowerShell** y ejecuta:

```powershell
cd C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Espera a ver:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ Backend corriendo en puerto 8000

---

### PASO 3: El Frontend Ya Está Corriendo

Tu frontend Angular ya está corriendo en `http://localhost:4200`

Ahora **recarga la página** (F5) y debería conectarse.

---

## 🧪 Verificar Conexión

1. **Abre el navegador**: http://localhost:4200
2. **Abre las DevTools** (F12)
3. **Recarga la página** (F5)
4. **En la consola NO deberías ver** errores de `ERR_CONNECTION_REFUSED`

Si ves la interfaz sin errores: ✅ **¡CONECTADO!**

---

## 🔍 Solución de Problemas

### "La base de datos no tiene tablas"

Necesitas poblar el sistema. Ejecuta:

```powershell
cd C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend
python scripts\poblar_sistema_completo.py
```

Esto creará:
- Tablas de usuarios, roles, permisos
- Tablas de niños
- Tablas de terapias
- Tablas de recomendaciones
- Tabla de fichas de emergencia
- Datos de ejemplo

### "ERROR 1045" al crear la BD

Usa phpMyAdmin (es más fácil):
1. http://localhost/phpmyadmin
2. Click "Nueva" (arriba a la izquierda)
3. Nombre: `autismo_mochis_ia`
4. Cotejamiento: `utf8mb4_general_ci`
5. Click "Crear"

### El backend muestra advertencias

Es normal ver:
```
⚠ ADVERTENCIA: GEMINI_API_KEY no está configurada
```

El sistema funciona sin problemas, solo no tendrás recomendaciones con IA (puedes configurarlo después).

---

## 📝 Comandos Resumidos

```powershell
# Terminal 1: Backend (dejar corriendo)
cd C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend (ya está corriendo)
# ng serve (YA ESTÁ ACTIVO)

# Terminal 3: Poblar datos (una sola vez)
cd C:\Users\crist\OneDrive\Escritorio\Version2\Autismo\backend
python scripts\poblar_sistema_completo.py
```

---

## 🎯 Checklist Rápido

- [ ] XAMPP MySQL iniciado
- [ ] Base de datos `autismo_mochis_ia` creada
- [ ] Backend corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 4200 (ya está)
- [ ] Navegador abierto en http://localhost:4200
- [ ] No hay errores `ERR_CONNECTION_REFUSED` en consola

**Cuando todos tengan ✅, el sistema está conectado.**

---

## 🆘 ¿Aún no funciona?

Comparte la salida de estos comandos:

```powershell
# Ver si el puerto 8000 está ocupado
netstat -ano | findstr :8000

# Ver procesos de Python
Get-Process python -ErrorAction SilentlyContinue

# Ver estado de MySQL
Get-Process mysqld -ErrorAction SilentlyContinue
```
