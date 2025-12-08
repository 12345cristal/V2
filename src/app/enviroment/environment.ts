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

  // SIN /api/v1 AQUÍ ❗
  apiBaseUrl: 'http://localhost:8000',

  apiUsuarios: 'http://localhost:8000/api/v1/usuarios',
  apiRoles: 'http://localhost:8000/api/v1/roles',
  apiPersonalSinUsuario: 'http://localhost:8000/api/v1/personal_sin_usuario',

  wsBaseUrl: 'ws://localhost:8000/ws'
};
