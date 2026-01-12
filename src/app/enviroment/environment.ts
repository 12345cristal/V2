

// src/environments/environment.ts
export const environment = {
  production: false,

  // ===============================
  // API REST (FastAPI)
  // ===============================
  apiBaseUrl: 'http://localhost:8000/api/v1',

  // ===============================
  // ARCHIVOS (fotos, CV, documentos)
  // ⚠️ NO lleva /api/v1
  // ===============================
  filesBaseUrl: 'http://localhost:8000/archivos',

  // ===============================
  // ENDPOINTS RELATIVOS
  // (se concatenan con apiBaseUrl)
  // ===============================
  apiUsuarios: '/usuarios',
  apiRoles: '/roles',
  apiPersonal: '/personal',
  apiPersonalSinUsuario: '/personal/sin-terapia',
  apiPerfil: '/perfil',

  // ===============================
  // WEBSOCKETS
  // ===============================
  wsBaseUrl: 'ws://localhost:8000/ws'
};
