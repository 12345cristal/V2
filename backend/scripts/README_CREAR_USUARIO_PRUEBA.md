# Script: Crear Usuario Padre de Prueba

Este script crea un usuario de prueba con rol de PADRE para testing del sistema.

## 📋 Requisitos Previos

1. **Base de datos configurada**: 
   - MySQL debe estar corriendo
   - La base de datos `autismo_mochis_ia` debe existir
   - Las tablas deben estar creadas (ejecuta las migraciones primero)

2. **Roles inicializados**:
   - Ejecuta primero: `python scripts/init_roles_permisos.py`
   - Esto crea los roles necesarios (Admin, Coordinador, Terapeuta, Padre)

3. **Archivo .env configurado**:
   - Verifica que `backend/.env` existe
   - Verifica que las credenciales de base de datos son correctas

## 🚀 Uso

### Desde el directorio backend:

```bash
cd backend
python scripts/crear_usuario_prueba.py
```

### O desde la raíz del proyecto:

```bash
cd V2
python backend/scripts/crear_usuario_prueba.py
```

## 👤 Usuario Creado

El script crea el siguiente usuario de prueba:

- **Email**: `lopez@padre.com`
- **Contraseña**: `12345678`
- **Rol**: Padre (ID: 4)
- **Nombre**: Lopez Padre Test
- **Teléfono**: 6681234567
- **Estado**: Activo

## 🔄 Comportamiento

### Si el usuario NO existe:
- Crea el usuario con los datos especificados
- Muestra un resumen del usuario creado

### Si el usuario YA existe:
- Muestra la información del usuario existente
- Pregunta si deseas actualizar la contraseña
- Si respondes 's', actualiza la contraseña a '12345678'
- Si respondes 'n', no hace cambios

## ✅ Resultado Esperado

```
============================================================
Crear Usuario Padre de Prueba
============================================================

✓ Rol encontrado: Padre (ID: 4)

============================================================
✓ Usuario lopez@padre.com creado exitosamente
============================================================
  ID: 5
  Nombre: Lopez Padre Test
  Email: lopez@padre.com
  Rol: Padre (ID: 4)
  Teléfono: 6681234567
  Estado: Activo
  Contraseña: 12345678
============================================================

✓ Ahora puedes usar estas credenciales para login en el frontend

✓ Proceso completado exitosamente
```

## 🧪 Testing del Login

Una vez creado el usuario, puedes probarlo en el frontend:

1. Inicia el frontend: `npm start` (desde el directorio raíz)
2. Ve a la página de login
3. Usa las credenciales:
   - Email: `lopez@padre.com`
   - Contraseña: `12345678`
4. Deberías acceder al dashboard de Padre

## ⚠️ Posibles Errores

### Error de conexión a la base de datos

```
❌ Error al conectar a la base de datos: (pymysql.err.OperationalError) ...
```

**Solución**:
1. Verifica que MySQL está corriendo
2. Verifica las credenciales en `.env`
3. Verifica que la base de datos existe

### Error: El rol Padre no existe

```
❌ Error: El rol Padre (ID=4) no existe en la base de datos
```

**Solución**:
Ejecuta primero el script de inicialización de roles:
```bash
python scripts/init_roles_permisos.py
```

## 📝 Notas

- Este es un usuario de **PRUEBA**, úsalo solo en desarrollo
- En producción, crea usuarios con contraseñas seguras
- El script usa bcrypt para hashear la contraseña de forma segura
- El script es idempotente: puedes ejecutarlo múltiples veces sin problemas
