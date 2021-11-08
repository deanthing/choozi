import { Injectable, NgModule } from '@angular/core';
import {
  BrowserModule,
  HammerModule,
  HammerGestureConfig,
  HAMMER_GESTURE_CONFIG,
} from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CodeComponent } from './components/code/code.component';
import { LandingComponent } from './components/landing/landing.component';
import { NameComponent } from './components/name/name.component';
import { PrefsComponent } from './components/prefs/prefs.component';
import { WaitingComponent } from './components/waiting/waiting.component';
import { SocketService } from './services/socket/socket.service';
import { CodeInputModule } from 'angular-code-input';
import { NgMultiSelectDropDownModule } from 'ng-multiselect-dropdown';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { SwipeUiComponent } from './components/swipe/swipe-ui/swipe-ui.component';
import { SwipeComponent } from './components/swipe/swipe.component';
import * as Hammer from 'hammerjs';

@Injectable()
export class MyHammerConfig extends HammerGestureConfig {
  overrides = <any>{
    pan: { direction: Hammer.DIRECTION_HORIZONTAL, threshold: 50 },
  };
}

@NgModule({
  declarations: [
    AppComponent,
    LandingComponent,
    PrefsComponent,
    NameComponent,
    CodeComponent,
    WaitingComponent,
    SwipeUiComponent,
    SwipeComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    RouterModule.forRoot([
      { path: '', component: LandingComponent },
      { path: 'prefs', component: PrefsComponent },
      { path: 'name', component: NameComponent },
      { path: 'code', component: CodeComponent },
      { path: 'waitingroom', component: WaitingComponent },
      { path: 'swipe', component: SwipeComponent },
    ]),
    CodeInputModule.forRoot({
      codeLength: 3,
      isCharsCode: true,
    }),
    NgMultiSelectDropDownModule.forRoot(),
    ReactiveFormsModule,
    HttpClientModule,
    HammerModule,
  ],
  providers: [
    SocketService,
    {
      provide: HAMMER_GESTURE_CONFIG,
      useClass: MyHammerConfig,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
