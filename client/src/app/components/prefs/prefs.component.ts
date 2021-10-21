import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { IDropdownSettings } from 'ng-multiselect-dropdown';
import { FormControl, FormGroup } from '@angular/forms';
import { StateService } from 'src/app/services/state/state.service';
import { ApiService } from 'src/app/services/api/api.service';
import {
  IUser,
  IMovie,
  IDropDownItem,
  IGenre,
  IGroup,
  IUserCreateRes,
} from 'src/models/userData';
import { map } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-prefs',
  templateUrl: './prefs.component.html',
  styleUrls: ['./prefs.component.css'],
})
export class PrefsComponent implements OnInit {
  // fields for drowdown forms
  genreDropdownList = [] as any;
  genreSelectedItems = [] as any;
  genreDropdownSettings = {} as IDropdownSettings;
  streamingDropdownList = [] as any;
  streamingSelectedItems = [] as any;
  streamingDropdownSettings = {} as IDropdownSettings;

  streamningData?: any;
  genreData?: any;

  form = new FormGroup({
    yearText: new FormControl(''),
    yearBeforeAfter: new FormControl(''),
  });

  constructor(
    private router: Router,
    private stateService: StateService,
    private apiService: ApiService,
    private http: HttpClient
  ) {
    console.log('constructor prefs', this.stateService.appPhase);
    this.reRoute();
  }

  ngOnInit(): void {
    this.initFormGenres();
    this.initFormStreaming();
  }

  onSubmit() {
    this.postGroup();
    this.stateService.appPhase = 'name';
    this.router.navigateByUrl('/name');
  }

  postGroup() {
    let genres = this.genreSelectedItems.map((item: any) => {
      return { name: item.name };
    });
    let providers = this.streamingSelectedItems.map((item: any) => {
      return { name: item.name };
    });

    let lower_bound = 0;
    let upper_bound = 0;
    if (this.form.value.yearText && this.form.value.yearBeforeAfter) {
      if (this.form.value.yearBeforeAfter === 'after') {
        lower_bound = this.form.value.yearText;
      } else {
        upper_bound = this.form.value.yearText;
      }
    }

    let to_post_group: IGroup = {
      streaming_providers: providers,
      genres: genres,
      release_period: { lower_bound: lower_bound, upper_bound: upper_bound },
    };

    this.apiService
      .postData<IGroup>('groups', to_post_group)
      .subscribe((resp) => {
        this.stateService.group = resp;
        this.stateService.user = {
          is_owner: true,
        };
        console.log(this.stateService.group);
      });
  }

  async initFormGenres() {
    this.apiService
      .getData('genres')
      .pipe(
        map((items: any) =>
          items.map((item: any) => {
            return { item_id: item.id, name: item.name };
          })
        )
      )
      .subscribe((res) => {
        this.genreDropdownList = res;
      });

    this.genreSelectedItems = [];
    this.genreDropdownSettings = {
      singleSelection: false,
      idField: 'item_id',
      textField: 'name',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      allowSearchFilter: true,
    };
  }

  initFormStreaming() {
    this.apiService
      .getData('streamingproviders')
      .pipe(
        map((items: any) =>
          items
            .filter((arr: any) => arr.display_priority < 13)
            .map((item: any) => {
              return { item_id: item.id, name: item.name };
            })
        )
      )
      .subscribe((res) => {
        this.streamingDropdownList = res;
      });
    this.streamingSelectedItems = [];
    this.streamingDropdownSettings = {
      singleSelection: false,
      idField: 'item_id',
      textField: 'name',
      selectAllText: 'Select All',
      unSelectAllText: 'UnSelect All',
      allowSearchFilter: true,
    };
  }

  reRoute() {
    let currentLoc = this.stateService.appPhase;

    if (currentLoc === '') {
      this.router.navigateByUrl('/');
    } else if (currentLoc === 'landing') {
      this.router.navigateByUrl('/');
    } else if (currentLoc === 'prefs') {
      return;
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
// https://www.npmjs.com/package/ng-multiselect-dropdown
