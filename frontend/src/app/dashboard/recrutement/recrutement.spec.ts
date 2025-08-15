import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Recrutement } from './recrutement';

describe('Recrutement', () => {
  let component: Recrutement;
  let fixture: ComponentFixture<Recrutement>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Recrutement]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Recrutement);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
