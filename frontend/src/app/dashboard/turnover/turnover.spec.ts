import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Turnover } from './turnover';

describe('Turnover', () => {
  let component: Turnover;
  let fixture: ComponentFixture<Turnover>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Turnover]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Turnover);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
