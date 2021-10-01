import { Component, OnInit } from '@angular/core';
import { CodeInputModule } from 'angular-code-input';
import { Router } from '@angular/router';
@Component({
  selector: 'app-code',
  templateUrl: './code.component.html',
  styleUrls: ['./code.component.css'],
})
export class CodeComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit(): void {}
  onCodeCompleted(code: string) {
    console.log('input complete:', code);
    this.router.navigateByUrl('/waitingroom');
  }
}

// https://www.npmjs.com/package/angular-code-input
