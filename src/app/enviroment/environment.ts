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

  // Base URL con /api/v1 para todos los módulos
  apiBaseUrl: 'http://localhost:8000/api/v1',

  // URLs relativas para usuarios (usar apiBaseUrl como prefijo)
  apiUsuarios: '/usuarios',
  apiRoles: '/roles',
  apiPersonalSinUsuario: '/personal/sin-terapia',

  wsBaseUrl: 'ws://localhost:8000/ws'
};
