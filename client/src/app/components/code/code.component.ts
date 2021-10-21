import { Component, OnInit } from '@angular/core';
import { CodeInputModule } from 'angular-code-input';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api/api.service';
import { StateService } from 'src/app/services/state/state.service';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
@Component({
  selector: 'app-code',
  templateUrl: './code.component.html',
  styleUrls: ['./code.component.css'],
})
export class CodeComponent implements OnInit {
  pinCode: any = '';
  errorText: any = 'Incorrect pin';
  isIncorrectPin: boolean = false;

  constructor(
    private router: Router,
    private apiService: ApiService,
    private stateService: StateService
  ) {
    this.reRoute();
  }

  ngOnInit(): void {}
  onCodeCompleted(code: string) {
    console.log('input complete:', this.pinCode);
    this.checkCode(this.pinCode);
  }

  onCodeChanged(code: string) {
    this.pinCode = code.toUpperCase();
  }

  checkCode(code: string) {
    this.apiService
      .getData('groups/code', code)
      .pipe(
        catchError((err) => {
          console.log('error');
          this.isIncorrectPin = true;
          return throwError(err);
        })
      )
      .subscribe((res) => {
        console.log(res);
        this.stateService.group = res;
        this.stateService.user = { is_owner: false };
        this.isIncorrectPin = false;
        this.stateService.appPhase = 'name';
        this.router.navigateByUrl('/name');
      });
  }

  reRoute() {
    let currentLoc = this.stateService.appPhase;

    if (currentLoc === '') {
      this.router.navigateByUrl('/');
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
    } else if (currentLoc === 'code') {
      this.router.navigateByUrl('/code');
    }
  }
}

// https://www.npmjs.com/package/angular-code-input
