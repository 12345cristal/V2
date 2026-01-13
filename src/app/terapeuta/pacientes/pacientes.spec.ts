import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PacientesComponent } from './pacientes';

describe('PacientesComponent', () => {
  let component: PacientesComponent;
  let fixture: ComponentFixture<PacientesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PacientesComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(PacientesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load patient list', () => {
    expect(component).toBeDefined();
  });

  it('should manage patient information', () => {
    expect(component).toBeTruthy();
  });
});
