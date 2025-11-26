import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { PersonalService } from '../../../service/personal.service';
import { Personal } from '../personal.interface';

@Component({
  selector: 'app-personal-list',
  standalone: true,
  templateUrl: './personal-list.html',
  styleUrls: ['./personal-list.scss'],
})
export class PersonalListComponent implements OnInit {
  
  personal: Personal[] = [];
  filtrados: Personal[] = [];
  roles: any[] = [];

  vistaActual: 'tarjetas' | 'tabla' | 'horarios' = 'tarjetas';

  constructor(
    private personalService: PersonalService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.conectarEventosUI();
    this.cargarRoles();
    this.cargarPersonal();
  }

  conectarEventosUI() {
  const tabs = [
    { id: 'tabTarjetas', vista: 'tarjetas' },
    { id: 'tabTabla', vista: 'tabla' },
    { id: 'tabHorarios', vista: 'horarios' }
  ];

  tabs.forEach(t => {
    document.getElementById(t.id)!.addEventListener('click', () => {
      this.cambiarVista(t.vista as any);
    });
  });

  // búsqueda
  document.getElementById('inputBuscar')!.addEventListener('input', () => this.filtrar());

  // roles
  document.getElementById('selectRol')!.addEventListener('change', () => this.filtrar());

  // CTRL + K
  document.addEventListener('keydown', (ev) => {
    if ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === 'k') {
      ev.preventDefault();
      const input = document.getElementById('inputBuscar') as HTMLInputElement;
      input.focus();
      input.select();
    }
  });
}


  cargarRoles() {
    this.personalService.getRoles().subscribe(data => {
      this.roles = data;

      const select = document.getElementById('selectRol') as HTMLSelectElement;
      select.innerHTML = '';

      const all = document.createElement('option');
      all.value = 'todos';
      all.textContent = 'Todos los roles';
      select.appendChild(all);

      data.forEach(r => {
        const op = document.createElement('option');
        op.value = r.nombre_rol;
        op.textContent = r.nombre_rol;
        select.appendChild(op);
      });
    });
  }

  cargarPersonal() {
    this.personalService.getPersonal().subscribe(data => {
      this.personal = data;
      this.filtrar();
    });
  }

  filtrar() {
    const txt = (document.getElementById('inputBuscar') as HTMLInputElement).value.toLowerCase();
    const rol = (document.getElementById('selectRol') as HTMLSelectElement).value;

    this.filtrados = this.personal.filter(p => {
      const coincideTexto =
        p.nombre_completo.toLowerCase().includes(txt) ||
        (p.especialidad_principal ?? '').toLowerCase().includes(txt);

      const coincideRol =
        rol === 'todos' || (p.especialidad_principal ?? '').toLowerCase() === rol.toLowerCase();

      return coincideTexto && coincideRol;
    });

    this.renderVista();
  }

 cambiarVista(v: 'tarjetas' | 'tabla' | 'horarios') {
  this.vistaActual = v;

  document.querySelectorAll('.tabs button')
    .forEach(b => b.classList.remove('active'));

  document.getElementById(`tab${v.charAt(0).toUpperCase() + v.slice(1)}`)!
    .classList.add('active');

  this.renderVista();
}


  renderVista() {
    (document.getElementById('contenedorTarjetas')!).style.display = 'none';
    (document.getElementById('contenedorTabla')!).style.display = 'none';
    (document.getElementById('contenedorHorarios')!).style.display = 'none';

    if (this.vistaActual === 'tarjetas') this.renderTarjetas();
    if (this.vistaActual === 'tabla') this.renderTabla();
    if (this.vistaActual === 'horarios') this.renderHorarios();
  }

  /* ==========================
          TARJETAS
  =========================== */
  renderTarjetas() {
    const cont = document.getElementById('contenedorTarjetas')!;
    cont.innerHTML = '';
    cont.style.display = 'grid';

    this.filtrados.forEach(p => {
      const card = document.createElement('div');
      card.classList.add('personal-card');

      card.innerHTML = `
        <div class="avatar">${p.nombre_completo.substring(0,2).toUpperCase()}</div>
        <h3>${p.nombre_completo}</h3>
        <p>${p.especialidad_principal ?? ''}</p>
        <p>${p.correo_personal ?? ''}</p>

        <button class="btn-edit">Editar</button>
      `;

      card.querySelector('.btn-edit')!.addEventListener('click', () =>
        this.router.navigate(['/coordinador/personal/editar', p.id_personal])
      );

      cont.appendChild(card);
    });
  }

  /* ==========================
            TABLA
  =========================== */
  renderTabla() {
    const cont = document.getElementById('contenedorTabla')!;
    cont.innerHTML = '';
    cont.style.display = 'block';

    const table = document.createElement('table');
    table.classList.add('tabla-personal');

    table.innerHTML = `
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Especialidad</th>
          <th>Correo</th>
          <th>Estado</th>
        </tr>
      </thead>
      <tbody></tbody>
    `;

    const tbody = table.querySelector('tbody')!;

    this.filtrados.forEach(p => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${p.nombre_completo}</td>
        <td>${p.especialidad_principal ?? '--'}</td>
        <td>${p.correo_personal ?? '--'}</td>
        <td>${p.activo ? 'Activo' : 'Inactivo'}</td>
      `;
      tbody.appendChild(tr);
    });

    cont.appendChild(table);
  }

  /* ==========================
          HORARIOS
  =========================== */
  renderHorarios() {
    const cont = document.getElementById('contenedorHorarios')!;
    cont.innerHTML = '';
    cont.style.display = 'block';

    this.filtrados.forEach(p => {
      const card = document.createElement('div');
      card.classList.add('horario-card');

      card.innerHTML = `
        <h3>${p.nombre_completo}</h3>
        <p>${p.especialidad_principal ?? ''}</p>
        <small>Horarios del personal irían aquí…</small>
      `;

      cont.appendChild(card);
    });
  }
}
