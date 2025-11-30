import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoNino } from './info-nino';

describe('InfoNino', () => {
  let component: InfoNino;
  let fixture: ComponentFixture<InfoNino>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InfoNino]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InfoNino);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
