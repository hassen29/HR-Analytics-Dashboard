import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Powerbi } from './powerbi';

describe('Powerbi', () => {
  let component: Powerbi;
  let fixture: ComponentFixture<Powerbi>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Powerbi]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Powerbi);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
