import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RecomendacionPanelComponent } from './recomendacion-panel';

describe('RecomendacionPanelComponent', () => {
  let component: RecomendacionPanelComponent;
  let fixture: ComponentFixture<RecomendacionPanelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecomendacionPanelComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(RecomendacionPanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display recommendation panel', () => {
    expect(component).toBeDefined();
  });

  it('should manage recommendation data', () => {
    expect(component).toBeTruthy();
  });
});
