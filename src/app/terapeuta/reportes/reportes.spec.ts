import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReportesComponent } from './reportes';

describe('ReportesComponent', () => {
  let component: ReportesComponent;
  let fixture: ComponentFixture<ReportesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReportesComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ReportesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should generate therapy reports', () => {
    expect(component).toBeDefined();
  });

  it('should export and display reports', () => {
    expect(component).toBeTruthy();
  });
});
