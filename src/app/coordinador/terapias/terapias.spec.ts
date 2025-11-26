import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Terapias } from './terapias';

describe('Terapias', () => {
  let component: Terapias;
  let fixture: ComponentFixture<Terapias>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Terapias]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Terapias);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
