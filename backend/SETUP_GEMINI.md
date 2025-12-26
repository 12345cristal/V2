# Configuración de Gemini AI

## Obtener API Key de Google Gemini

1. Ve a [Google AI Studio](https://aistudio.google.com/apikey)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en "Get API Key" o "Create API Key"
4. Copia la API key generada

## Configurar en el Backend

Crea o edita el archivo `.env` en la carpeta `backend/`:

```env
# Gemini AI
GEMINI_API_KEY=tu_api_key_aqui
```

## Reiniciar el Backend

Después de configurar la API key, reinicia el backend:

```powershell
cd backend
./start.ps1
```

## Verificar Configuración

1. Abre http://localhost:8000/docs
2. Ve al endpoint `/api/v1/ia/estado`
3. Haz clic en "Try it out" y luego "Execute"
4. Deberías ver `"configurado": true` en la respuesta

## Sin API Key

Si no configuras la API key, el chatbot funcionará en modo fallback con respuestas generales predefinidas.
