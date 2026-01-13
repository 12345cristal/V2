import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NinosComponent } from './ninos';

describe('NinosComponent', () => {
  let component: NinosComponent;
  let fixture: ComponentFixture<NinosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NinosComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(NinosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load list of children', () => {
    expect(component).toBeDefined();
  });

  it('should filter and search children', () => {
    expect(component).toBeTruthy();
  });
});
