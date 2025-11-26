import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Ninos } from './ninos';

describe('Ninos', () => {
  let component: Ninos;
  let fixture: ComponentFixture<Ninos>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Ninos]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Ninos);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
