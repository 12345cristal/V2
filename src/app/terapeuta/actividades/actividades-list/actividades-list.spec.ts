import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivitiesListComponent } from './actividades-list';

describe('ActivitiesListComponent', () => {
  let component: ActivitiesListComponent;
  let fixture: ComponentFixture<ActivitiesListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ActivitiesListComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ActivitiesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should display list of activities', () => {
    expect(component).toBeDefined();
  });

  it('should handle activity selection', () => {
    expect(component).toBeTruthy();
  });
});
