import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictAttrition } from './predict-attrition';

describe('PredictAttrition', () => {
  let component: PredictAttrition;
  let fixture: ComponentFixture<PredictAttrition>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PredictAttrition]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PredictAttrition);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
