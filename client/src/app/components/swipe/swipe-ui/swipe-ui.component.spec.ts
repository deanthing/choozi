import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SwipeUiComponent } from './swipe-ui.component';

describe('SwipeUiComponent', () => {
  let component: SwipeUiComponent;
  let fixture: ComponentFixture<SwipeUiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SwipeUiComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SwipeUiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
