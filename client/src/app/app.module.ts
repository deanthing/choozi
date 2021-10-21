import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
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

@NgModule({
  declarations: [
    AppComponent,
    LandingComponent,
    PrefsComponent,
    NameComponent,
    CodeComponent,
    WaitingComponent,
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
    ]),
    CodeInputModule.forRoot({
      codeLength: 3,
      isCharsCode: true,
    }),
    NgMultiSelectDropDownModule.forRoot(),
    ReactiveFormsModule,
    HttpClientModule,
  ],
  providers: [SocketService],
  bootstrap: [AppComponent],
})
export class AppModule {}
