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
    this.pullMovies();
  }

  ngOnInit(): void {
    this.subscribeToSockets();
  }

  moveRecsToFrontOfStore() {
    const recs = this.stateService.group?.movies!.slice(44);
    this.movieStore = [...recs!].concat(this.movieStore);
  }

  pullMovies() {
    this.movieStore = this.stateService.group!.movies!;
    this.addMoviesFromStore();
  }

  postChoice(choice: any) {
    this.cardCountCheck();
    this.storeCountCheck();

    if (choice.choice) {
      let likeCreate: ILikeCreate = {
        group_id: this.stateService.group?.id!,
        movie_id: choice.payload.id,
      };

      // post like
      this.apiService
        .postData<ILikeCreate>('likes', likeCreate)
        .subscribe(() => console.log('like posted'));

      // generate recs, then emit that recs have been created to group
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
    }
  }

  cardCountCheck() {
    if (this.cards.length <= 5) {
      // pull first 15 cards from store to card stack
      this.addMoviesFromStore();
    }
  }

  foundLikeCheck() {
    // get number of users in group
    // find duplicates where all users have liked the same movie
    var counts: number[] = [];
    var likes: ILike[] = [];
    this.apiService.getData('likes', this.stateService.user?.group_id!);

    likes.forEach((element: ILike) => {
      if (counts[element.group_id] == undefined) {
        counts[element.group_id] = 1;
      } else {
        counts[element.group_id]++;
      }
    });

    likes.forEach((likes: ILike) => {
      // find movie with likes equal to number of people in group
    });
  }

  storeCountCheck() {
    if (this.movieStore.length <= 15) {
      // remove old movies from store and db
      this.apiService
        .deleteData('moviesforgroup', this.stateService.user?.group_id)
        .subscribe((data) => {
          console.log('deleted group movies');
        });

      // generate movies for store (not recs, just movies that match search paramaters)
      this.apiService
        .getData('moviegen', this.stateService.group!.id)
        .subscribe((group: IGroup) => {
          console.log('movies generated');
          this.socketService.emit(
            'newMovies',
            this.stateService.user?.group_id!
          );
        });
    }
  }

  addMoviesFromStore() {
    // pop 10 movies from store to cards
    this.cards.push(
      ...this.movieStore.slice(0, 15).sort(() => (Math.random() > 0.5 ? 1 : -1))
    );

    // remove the 10 movies from store
    this.movieStore = this.movieStore.filter(
      (movie) => !this.cards.includes(movie)
    );
  }

  subscribeToSockets() {
    // when a user generates reccomendations
    this.socketService.recieveEmit('newRecs').subscribe((data) => {
      this.apiService
        .getData('group', this.stateService.user?.group_id!)
        .subscribe((group: IGroup) => {
          this.stateService.group = group;
          this.moveRecsToFrontOfStore();
        });
    });

    // when a user runs out and generates new movies
    this.socketService.recieveEmit('newMovies').subscribe((data) => {
      this.apiService
        .getData('group', this.stateService.user?.group_id!)
        .subscribe((group: IGroup) => {
          this.stateService.group = group;
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
