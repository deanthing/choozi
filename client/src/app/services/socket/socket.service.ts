import { Injectable } from '@angular/core';
// import { Socket } from 'ngx-socket-io';
import { Observable, Observer, Subscriber } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { io, Socket } from 'socket.io-client';
// https://stackoverflow.com/questions/59586160/multiple-socket-io-connections-in-angular-8
@Injectable({
  providedIn: 'root',
})
export class SocketService {
  socket: Socket;

  constructor() {
    this.socket = io('ws://127.0.0.1:8000', {
      path: '/ws/socket.io',
      autoConnect: false,
    });
    this.connectSocket();
  }

  async connectSocket() {
    console.log('socket connectiong');
    return this.socket.connect();
  }

  emit(event: string, data: any) {
    this.socket.emit(event, data);
  }

  recieveEmit(eventName: string): Observable<any> {
    return new Observable<any>((subscriber: Observer<any>) => {
      this.socket.on(eventName, (event) => {
        subscriber.next(event);
      });
      return () => {
        // tearDownLogic, i.e. code executed when this Observable is unsubscribed
      };
    });
  }
}
