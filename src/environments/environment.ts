export const environment = {
  production: false,

  // ===============================
  // API REST (FastAPI)
  // ===============================
  // TODAS las rutas del backend están bajo /api/v1
  apiBaseUrl: 'http://localhost:8000/api/v1',

  // ===============================
  // ARCHIVOS (uploads estáticos)
  // ⚠️ NO lleva /api/v1
  // ===============================
  filesBaseUrl: 'http://localhost:8000/uploads',

  // ===============================
  // WEBSOCKETS
  // ===============================
  wsBaseUrl: 'ws://localhost:8000/ws',


};
