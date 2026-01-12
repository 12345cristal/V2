// src/environments/environment.ts
export const environment = {
  production: false,

  // ===============================
  // API REST (FastAPI)
  // ===============================
  apiBaseUrl: 'http://localhost:8000/api',

  // ===============================
  // ARCHIVOS (fotos, CV, documentos)
  // ⚠️ NO lleva /api/v1
  // ===============================
  filesBaseUrl: 'http://localhost:8000/uploads',

  // ===============================
  // ENDPOINTS RELATIVOS
  // (se concatenan con apiBaseUrl)
  // ===============================
  apiUsuarios: 'http://localhost:8000/api/usuarios',
  apiRoles: 'http://localhost:8000/api/roles',
  apiPersonal: 'http://localhost:8000/api/personal',
  apiPersonalSinUsuario: 'http://localhost:8000/api/personal/sin-usuario',
  apiPerfil: 'http://localhost:8000/api/perfil',

  // ===============================
  // WEBSOCKETS
  // ===============================
  wsBaseUrl: 'ws://localhost:8000',

  // ===============================
  // Nueva API URL
  // ===============================
  apiUrl: 'http://localhost:8000'
};
