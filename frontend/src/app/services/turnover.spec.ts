import { TestBed } from '@angular/core/testing';

import { Turnover } from './turnover';

describe('Turnover', () => {
  let service: Turnover;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Turnover);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
