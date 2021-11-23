import { Message } from '@angular/compiler/src/i18n/i18n_ast';
import { Component, OnInit } from '@angular/core';
import { SocketService } from 'src/app/services/socket/socket.service';
import { Router } from '@angular/router';
import { StateService } from 'src/app/services/state/state.service';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css'],
})
export class LandingComponent implements OnInit {
  constructor(
    private socketService: SocketService,
    private router: Router,
    private stateService: StateService
  ) {
    console.log('constructor landing', this.stateService.appPhase);

    if (this.stateService.appPhase === '') {
      this.stateService.appPhase = 'landing';
    }
    console.log('constructor landing', this.stateService.appPhase);

    this.reRoute();
  }

  ngOnInit(): void {}

  onJoin() {
    this.router.navigateByUrl('/code');
  }

  onSwipe() {
    this.router.navigateByUrl('/swipe');
  }

  onCreate() {
    this.stateService.appPhase = 'prefs';
    this.router.navigateByUrl('/prefs');
  }

  reRoute() {
    let currentLoc = this.stateService.appPhase;

    if (currentLoc === 'landing') {
      return;
    } else if (currentLoc === 'prefs') {
      this.router.navigateByUrl('/prefs');
    } else if (currentLoc === 'name') {
      this.router.navigateByUrl('/name');
    } else if (currentLoc === 'waitingroom') {
      this.router.navigateByUrl('/waitingroom');
    } else if (currentLoc === 'round') {
      this.router.navigateByUrl('/round');
    } else if (currentLoc === 'results') {
      this.router.navigateByUrl('/results');
    }
  }
}
