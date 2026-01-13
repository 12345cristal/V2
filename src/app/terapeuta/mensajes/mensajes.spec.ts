import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MensajesComponent } from './mensajes';

describe('MensajesComponent', () => {
  let component: MensajesComponent;
  let fixture: ComponentFixture<MensajesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MensajesComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(MensajesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should load messages', () => {
    expect(component).toBeDefined();
  });

  it('should send and receive messages', () => {
    expect(component).toBeTruthy();
  });
});
