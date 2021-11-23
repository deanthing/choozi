import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api/api.service';
import { SocketService } from 'src/app/services/socket/socket.service';
import { StateService } from 'src/app/services/state/state.service';
import { IGroup, ILikeCreate, IMovie, ILike } from 'src/models/userData';

@Component({
  selector: 'app-swipe',
  templateUrl: './swipe.component.html',
  styleUrls: ['./swipe.component.css'],
})
export class SwipeComponent implements OnInit {
  cards: IMovie[] = [];
  movieStore: IMovie[] = [];

  constructor(
    private apiService: ApiService,
    private stateService: StateService,
    private router: Router,
    private socketService: SocketService
  ) {
    this.reRoute();
    this.updateStoreFromState();
    this.addMoviesFromStore();
  }

  ngOnInit(): void {
    this.subscribeToSockets();
  }

  moveRecsToFrontOfStore() {
    console.log('moving recs to front of store');
    const recs = this.stateService.group?.movies!.slice(44);
    this.movieStore = [...recs!].concat(this.movieStore);
  }

  updateStoreFromState() {
    console.log('updating store from state service group');
    this.movieStore = this.stateService.group!.movies!;
    console.log('movie store after pulling newly generated', this.movieStore);
    // this.addMoviesFromStore();
    // this ^ shouldnt be here, jsut becaues the store was updated doesnt mean that the card need to be updated, it will update the cards when necessary
  }

  postChoice(choice: any) {
    this.storeCountCheck();
    this.cardCountCheck();

    if (choice.choice) {
      console.log('a like has happened!');
      let likeCreate: ILikeCreate = {
        group_id: this.stateService.group?.id!,
        movie_id: choice.payload.id,
      };

      // post like
      this.apiService
        .postData<ILikeCreate>('likes', likeCreate)
        .subscribe(() => {
          console.log('like posted');
          this.apiService
            .getData('movierecs', this.stateService.user?.group_id)
            .subscribe((group: IGroup) => {
              this.stateService.group = group;
              console.log('reccomendations pulled');
              this.socketService.emit(
                'recsInserted',
                this.stateService.user?.group_id!
              );
            });
        });

      // generate recs, then emit that recs have been created to group
    }
  }

  cardCountCheck() {
    if (this.cards.length == 5) {
      // pull first 15 cards from store to card stack
      console.log('5 cards left');
      this.addMoviesFromStore();
    }
  }

  storeCountCheck() {
    if (this.movieStore.length <= 15) {
      console.log('store has less than equal to 15');
      // remove old movies from store and db
      this.apiService
        .deleteData('moviesforgroup', this.stateService.user?.group_id!)
        .subscribe((data) => {
          console.log('deleted group movies');
          this.apiService
            .getData('moviegen', this.stateService.group!.id)
            .subscribe((group: IGroup) => {
              console.log(
                'movies generated for',
                this.stateService.user?.group_id!
              );
              this.socketService.emit(
                'newMovies',
                this.stateService.user?.group_id!
              );
            });
        });
    } else if (this.movieStore.length > 45) {
      this.movieStore = this.movieStore.slice(0, 44);
    }
  }

  addMoviesFromStore() {
    console.log('cards before adding from store:', this.cards);
    console.log('adding moveies from store');
    // pop 10 movies from store to cards
    this.cards.push(
      ...this.movieStore.slice(0, 15).sort(() => (Math.random() > 0.5 ? 1 : -1))
    );

    console.log('cards after adding from store:', this.cards);

    // remove the movies from store
    this.movieStore = this.movieStore.filter(
      (movie) => !this.cards.includes(movie)
    );
  }

  subscribeToSockets() {
    // when a user generates reccomendations
    this.socketService.recieveEmit('newRecs').subscribe((data) => {
      console.log('receiverd emit for new recs');
      this.apiService
        .getData('groups', this.stateService.user?.group_id!)
        .subscribe((group: IGroup) => {
          this.stateService.group = group;
          this.moveRecsToFrontOfStore();
        });
    });

    // when a user runs out and generates new movies
    this.socketService.recieveEmit('newMoviesGenerated').subscribe((data) => {
      console.log('receivomg new movies (not recs)');

      this.apiService
        .getData('groups', this.stateService.user?.group_id!)
        .subscribe((group: IGroup) => {
          console.log('movies generated receieved', group);
          this.stateService.group = group;
          this.updateStoreFromState();
        });
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
      this.router.navigateByUrl('/swipe');
    } else if (currentLoc === 'round') {
      this.router.navigateByUrl('/round');
    } else if (currentLoc === 'results') {
      this.router.navigateByUrl('/results');
    } else if (currentLoc === 'code') {
      this.router.navigateByUrl('/code');
    } else if (currentLoc === 'swipe') {
      this.router.navigateByUrl('/swipe');
    }
  }
}
