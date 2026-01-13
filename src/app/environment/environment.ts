// // export const environment = {
// //   production: false,
// //   apiBaseUrl: 'http://localhost:8000/api/v1',

// //   apiUsuarios: '/usuarios',
// //   apiRoles: '/roles',
// //   apiPersonalSinUsuario: '/personal/sin-usuario'
// // };



// export const environment = {
//   production: false,
//   apiBaseUrl: 'http://localhost:8000/api/v1',
//   apiUsuarios: 'http://localhost:8000/api/usuarios',
//   apiRoles: 'http://localhost:8000/api/roles',
//   apiPersonalSinUsuario: 'http://localhost:8000/api/personal_sin_usuario',
//   wsBaseUrl: 'ws://localhost:8000/ws'  // <- agrega esto
// };


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
  apiRoles: '/catalogos/roles',
  apiPersonal: '/personal',
  apiPersonalSinUsuario: '/personal/sin-usuario',
  apiPerfil: '/perfil',

  // ===============================
  // WEBSOCKETS
  // ===============================
  wsBaseUrl: 'ws://localhost:8000/ws'
};
