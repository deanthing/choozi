import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-waiting',
  templateUrl: './waiting.component.html',
  styleUrls: ['./waiting.component.css'],
})
export class WaitingComponent implements OnInit {
  entryCode: string = '';
  entryLink: string = '';
  constructor() {}

  ngOnInit(): void {
    this.initEntryInformation();
  }

  initEntryInformation() {
    this.entryCode = 'ABC';
    this.entryLink = 'asdf.com';
  }
}
