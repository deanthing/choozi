import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { ApiService } from 'src/app/services/api/api.service';
import { SocketService } from 'src/app/services/socket/socket.service';
import { StateService } from 'src/app/services/state/state.service';
import { IGroup, IUser } from 'src/models/userData';
import { map } from 'rxjs/operators';

@Component({
  selector: 'app-waiting',
  templateUrl: './waiting.component.html',
  styleUrls: ['./waiting.component.css'],
})
export class WaitingComponent implements OnInit {
  entryCode: string = '';
  entryLink: string = '';
  usersJoined: IUser[] = [];
  isOwner?: boolean;
  userId?: number;
  moviesGenerated: boolean = false;

  constructor(
    private apiService: ApiService,
    private router: Router,
    private stateService: StateService,
    private socketService: SocketService
  ) {
    this.reRoute();
    this.isOwner = this.stateService.user?.is_owner;
    this.userId = this.stateService.user?.id;
  }

  ngOnInit() {
    this.initEntryInformation();
    this.loadUsers();
    this.initSockets();
    this.generateMovies();
  }

  generateMovies() {
    // gen movies
    if (this.stateService.user?.is_owner) {
      this.apiService
        .getData('moviegen', this.stateService.group!.id)
        .subscribe((group: IGroup) => {
          console.log('movies generated');
          this.stateService.group = group;
          this.moviesGenerated = true;
        });
    }
  }

  removeUser(user: IUser) {
    console.log(user);
    this.socketService.emit('deleteUser', JSON.stringify(user));
    this.apiService
      .deleteData('users', user.id)
      .subscribe(() => console.log('deleted user'));
  }

  initSockets() {
    this.socketService
      .recieveEmit('joinRoom')
      .pipe(
        map((user: any) => {
          return JSON.parse(user);
        })
      )
      .subscribe((user: IUser) => {
        console.log(user.id + ' ' + this.stateService.user?.id);
        if (user.id != this.stateService.user?.id) {
          this.usersJoined.push(user);
        }
      });

    this.socketService
      .recieveEmit('removeUser')
      // .pipe(
      //   map((user: any) => {
      //     return JSON.parse(user);
      //   })
      // )
      .subscribe((user: IUser) => {
        console.log('removeUser socket call for', user);
        if (user.id == this.stateService.user?.id) {
          this.socketService.emit('removeMe', user);
          this.stateService.resetState();
          this.router.navigateByUrl('/');
          console.log('remove this user');
        } else {
          this.usersJoined = this.usersJoined.filter(
            (userToRemove) => userToRemove.id == this.stateService.user?.id
          );

          if (this.stateService.group?.users) {
            this.stateService.group!.users =
              this.stateService.group.users.filter(
                () => user.id != this.stateService.user?.id
              );
          }
        }
      });

    this.socketService
      .recieveEmit('roomClosed')
      // .pipe(
      //   map((user: any) => {
      //     return JSON.parse(user);
      //   })
      // )
      .subscribe((data) => {
        this.stateService.resetState();
        this.router.navigateByUrl('/');
      });

    this.socketService
      .recieveEmit('roomStarted')
      // .pipe(
      //   map((user: any) => {
      //     return JSON.parse(user);
      //   })
      // )
      .subscribe((data) => {
        this.stateService.appPhase = 'swipe';
        this.router.navigateByUrl('/swipe');
      });
  }

  leaveRoom() {
    let user = this.stateService.user!;
    this.socketService.emit('deleteUser', JSON.stringify(user));
    this.apiService
      .deleteData('users', user.id)
      .subscribe(() => console.log('deleted user'));
  }
  closeRoom() {
    // post delete group
    this.apiService
      .getData('deletegroup', this.stateService.group!.id)
      .subscribe(() => console.log('group deleted'));
    // emit close room
    this.socketService.emit('closeRoom', this.stateService.group!.id);
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
        const users: IUser[] = res.users.map((user: any) => {
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
    // TODO: need to setup variable routing for this
  }

  onStartRound() {
    this.socketService.emit('startRoom', this.stateService.user?.group_id);
    this.stateService.appPhase = 'swipe';
    this.router.navigateByUrl('/swipe');
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
