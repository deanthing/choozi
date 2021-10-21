import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { ApiService } from 'src/app/services/api/api.service';
import { SocketService } from 'src/app/services/socket/socket.service';
import { StateService } from 'src/app/services/state/state.service';
import { IUser } from 'src/models/userData';
import { map } from 'rxjs/operators';

interface IWaitingRoomUser {
  id: number;
  name: string;
}

@Component({
  selector: 'app-waiting',
  templateUrl: './waiting.component.html',
  styleUrls: ['./waiting.component.css'],
})
export class WaitingComponent implements OnInit {
  entryCode: string = '';
  entryLink: string = '';
  usersJoined: IWaitingRoomUser[] = [];
  constructor(
    private apiService: ApiService,
    private router: Router,
    private stateService: StateService,
    private socketService: SocketService
  ) {
    this.reRoute();
  }

  ngOnInit() {
    this.initEntryInformation();
    this.loadUsers();
    this.initSockets();
  }

  removeUser(user: IWaitingRoomUser) {
    this.apiService.deleteData('users', user.id);
  }

  initSockets() {
    this.socketService
      .recieveEmit('joinRoom')
      .pipe(
        map((user: any) => {
          return JSON.parse(user);
        })
      )
      .subscribe((user: IWaitingRoomUser) => {
        if (user.id != this.stateService.user?.id) {
          this.usersJoined.push({ id: user.id, name: user.name });
        }
      });

    this.socketService
      .recieveEmit('removeUser')
      .pipe(
        map((user: any) => {
          return JSON.parse(user);
        })
      )
      .subscribe((user: IWaitingRoomUser) => {
        if (user.id != this.stateService.user?.id) {
          this.usersJoined.push({ id: user.id, name: user.name });
        }
      });
  }

  loadUsers() {
    this.apiService
      .getData('groups', this.stateService.group?.id)
      .pipe(
        catchError((err) => {
          console.log('error');
          return throwError(err);
        })
      )
      .subscribe((res) => {
        console.log(res.users);
        this.stateService.group = res;
        const users: IWaitingRoomUser[] = res.users.map((user: any) => {
          console.log('user in for loop', user);
          return { name: user.name, id: user.id };
        });
        console.log('users pulled', users);
        this.usersJoined = this.usersJoined.concat(users);
      });
  }

  initEntryInformation() {
    let group = this.stateService.group;
    if (group?.room_code) {
      this.entryLink =
        window.location.protocol + window.location.host + '/' + group.room_code;
      this.entryCode = group.room_code;
    }
    {
      console.log('group not initialized');
    }
    // need to setup variable routing for this
  }

  onStartRound() {
    this.stateService.appPhase = 'waitingroom';
    this.router.navigateByUrl('/round');
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
      return;
    } else if (currentLoc === 'round') {
      this.router.navigateByUrl('/round');
    } else if (currentLoc === 'results') {
      this.router.navigateByUrl('/results');
    } else if (currentLoc === 'code') {
      this.router.navigateByUrl('/code');
    }
  }
}
