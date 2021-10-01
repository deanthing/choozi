import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrefsComponent } from './prefs.component';

describe('PrefsComponent', () => {
  let component: PrefsComponent;
  let fixture: ComponentFixture<PrefsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PrefsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PrefsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
