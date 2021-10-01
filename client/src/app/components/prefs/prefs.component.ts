import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { IDropdownSettings } from 'ng-multiselect-dropdown';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-prefs',
  templateUrl: './prefs.component.html',
  styleUrls: ['./prefs.component.css'],
})
export class PrefsComponent implements OnInit {
  genreDropdownList = [] as any;
  genreSelectedItems = [] as any;
  genreDropdownSettings = {} as IDropdownSettings;
  streamingDropdownList = [] as any;
  streamingSelectedItems = [] as any;
  streamingDropdownSettings = {} as IDropdownSettings;
  yearNumber = '' as string;
  yearBefore: boolean;
  yearAfter: boolean;

  form = new FormGroup({
    yearText: new FormControl(''),
    yearBeforeAfter: new FormControl(''),
  });

  constructor(private router: Router) {
    this.yearAfter = false;
    this.yearBefore = false;
  }

  ngOnInit(): void {
    this.initFormGenres();
    this.initFormStreaming();
  }

  onStart() {
    console.log(
      this.form.value,
      this.streamingSelectedItems,
      this.genreSelectedItems
    );
    this.router.navigateByUrl('/name');
  }
  initFormGenres() {
    this.genreDropdownList = [
      { item_id: 1, item_text: 'Mumbai' },
      { item_id: 2, item_text: 'Bangaluru' },
      { item_id: 3, item_text: 'Pune' },
      { item_id: 4, item_text: 'Navsari' },
      { item_id: 5, item_text: 'New Delhi' },
    ];
    this.genreSelectedItems = [];
    this.genreDropdownSettings = {
      singleSelection: false,
      idField: 'item_id',
      textField: 'item_text',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      allowSearchFilter: true,
    };
  }

  initFormStreaming() {
    this.streamingDropdownList = [
      { item_id: 1, item_text: 'Mumbai' },
      { item_id: 2, item_text: 'Bangaluru' },
      { item_id: 3, item_text: 'Pune' },
      { item_id: 4, item_text: 'Navsari' },
      { item_id: 5, item_text: 'New Delhi' },
    ];
    this.streamingSelectedItems = [];
    this.streamingDropdownSettings = {
      singleSelection: false,
      idField: 'item_id',
      textField: 'item_text',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      allowSearchFilter: true,
    };
  }
}
// https://www.npmjs.com/package/ng-multiselect-dropdown
