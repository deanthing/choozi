import { ViewFlags } from '@angular/compiler/src/core';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api/api.service';
import { StateService } from 'src/app/services/state/state.service';
import { IUser, IUserCreateRes } from 'src/models/userData';
import { map } from 'rxjs/operators';
import { SocketService } from 'src/app/services/socket/socket.service';

@Component({
  selector: 'app-name',
  templateUrl: './name.component.html',
  styleUrls: ['./name.component.css'],
})
export class NameComponent implements OnInit {
  form = new FormGroup({
    name: new FormControl('', [Validators.required]),
  });

  nameNull = false;

  groupData?: any;
  constructor(
    private router: Router,
    private apiService: ApiService,
    private stateService: StateService,
    private socketService: SocketService
  ) {}

  ngOnInit(): void {
    this.reRoute();
  }

  onStart() {
    if (this.form.value.name) {
      console.log('objecvaluet');
      this.postUser();
    } else {
      this.nameNull = true;
    }
  }

  postUser() {
    let group = this.stateService.group;
    let user = this.stateService.user;
    if (group && user) {
      let to_post_user: IUser = {
        ...user,
        name: this.form.value.name,
        group_id: group.id,
      };
      console.log(to_post_user);
      this.apiService
        .postData<IUserCreateRes>('users', to_post_user)
        .subscribe((res: any) => {
          console.log(res);
          this.stateService.user = res.user;
          this.stateService.token = res.token;
          this.addUserToGroupSocket();
          this.stateService.appPhase = 'waitingroom';
          this.router.navigateByUrl('/waitingroom');
        });
    } else {
      console.log("Group or user not defined, can't post");
    }
  }

  addUserToGroupSocket() {
    if (this.stateService.user) {
      let data = {
        group_id: this.stateService.user.group_id,
        id: this.stateService.user.id,
        name: this.stateService.user.name,
      };
      this.socketService.emit('joinRoom', data);
    }
  }

  reRoute() {
    let currentLoc = this.stateService.appPhase;

    if (currentLoc === '') {
      this.router.navigateByUrl('/');
    } else if (currentLoc === 'prefs') {
      this.router.navigateByUrl('/prefs');
    } else if (currentLoc === 'name') {
      return;
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
