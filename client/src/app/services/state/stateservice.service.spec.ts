import { TestBed } from '@angular/core/testing';

import { StateserviceService } from './stateservice.service';

describe('StateserviceService', () => {
  let service: StateserviceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StateserviceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
