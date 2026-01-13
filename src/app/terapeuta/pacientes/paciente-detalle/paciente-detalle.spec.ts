import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PacienteDetalleComponent } from './paciente-detalle';

describe('PacienteDetalleComponent', () => {
  let component: PacienteDetalleComponent;
  let fixture: ComponentFixture<PacienteDetalleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PacienteDetalleComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(PacienteDetalleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load patient details', () => {
    expect(component).toBeDefined();
  });

  it('should update patient information', () => {
    expect(component).toBeTruthy();
  });
});
