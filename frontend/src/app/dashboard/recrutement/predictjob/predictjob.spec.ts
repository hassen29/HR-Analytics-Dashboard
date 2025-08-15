import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Predictjob } from './predictjob';

describe('Predictjob', () => {
  let component: Predictjob;
  let fixture: ComponentFixture<Predictjob>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Predictjob]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Predictjob);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
