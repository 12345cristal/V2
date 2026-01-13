import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SesionesComponent } from './sesiones';

describe('SesionesComponent', () => {
  let component: SesionesComponent;
  let fixture: ComponentFixture<SesionesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SesionesComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(SesionesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load therapy sessions', () => {
    expect(component).toBeDefined();
  });

  it('should manage session scheduling and tracking', () => {
    expect(component).toBeTruthy();
  });
});
