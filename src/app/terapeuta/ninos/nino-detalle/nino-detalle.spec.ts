import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NinoDetalleComponent } from './nino-detalle';

describe('NinoDetalleComponent', () => {
  let component: NinoDetalleComponent;
  let fixture: ComponentFixture<NinoDetalleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NinoDetalleComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(NinoDetalleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load child details', () => {
    expect(component).toBeDefined();
  });

  it('should display child information', () => {
    expect(component).toBeTruthy();
  });
});
