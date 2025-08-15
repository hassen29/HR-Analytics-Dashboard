import { TestBed } from '@angular/core/testing';

import { Recrutement } from './recrutement';

describe('Recrutement', () => {
  let service: Recrutement;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Recrutement);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
