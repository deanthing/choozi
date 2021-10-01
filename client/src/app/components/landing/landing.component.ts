import { Message } from '@angular/compiler/src/i18n/i18n_ast';
import { Component, OnInit } from '@angular/core';
import { SocketService } from 'src/app/services/socket/socket.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css'],
})
export class LandingComponent implements OnInit {
  constructor(private socketService: SocketService, private router: Router) {}

  ngOnInit(): void {
    // this.socketService.connectSocket();
  }
  onJoin() {
    this.router.navigateByUrl('/code');
    // console.log('objecclickt');
    // this.socketService.emit('joinRoom', 6969);
  }

  onCreate() {
    this.router.navigateByUrl('/prefs');
  }

  sendMessage(): void {}
}
