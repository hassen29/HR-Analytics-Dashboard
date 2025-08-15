import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListCandidat } from './list-candidat';

describe('ListCandidat', () => {
  let component: ListCandidat;
  let fixture: ComponentFixture<ListCandidat>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListCandidat]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListCandidat);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
