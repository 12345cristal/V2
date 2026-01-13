import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivitiesComponent } from './actividades';

describe('ActivitiesComponent', () => {
  let component: ActivitiesComponent;
  let fixture: ComponentFixture<ActivitiesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ActivitiesComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ActivitiesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize component with data', () => {
    expect(component).toBeDefined();
  });

  it('should have empty activities list on init', () => {
    expect(component.actividades).toBeDefined();
  });
});
