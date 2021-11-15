import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from 'src/app/services/api/api.service';
import { StateService } from 'src/app/services/state/state.service';
import { IGroup, ILikeCreate, IMovie } from 'src/models/userData';

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
    private router: Router
  ) {
    this.reRoute();
    this.pullMovies();
  }

  ngOnInit(): void {}

  pullMovies() {
    console.log(this.stateService.group!.movies!);
    this.movieStore = this.stateService.group!.movies!;
    this.addMoviesFromStore();
  }

  postChoice(choice: any) {
    console.log(this.cards);
    if (choice.choice) {
      let likeCreate: ILikeCreate = {
        group_id: this.stateService.group?.id!,
        movie_id: choice.payload.id,
      };
      this.apiService
        .postData<ILikeCreate>('likes', likeCreate)
        .subscribe(() => console.log('like posted'));
    }
  }

  cardCountCheck() {
    if (this.movieStore.length <= 10) {
      // generate movies for store
      // remove old movies from store
      // generate movies from likes
    }

    if (this.cards.length <= 4) {
    }
  }

  addMoviesFromStore() {
    // pop 10 movies from store to cards
    this.cards = this.movieStore
      .slice(0, 9)
      .sort(() => (Math.random() > 0.5 ? 1 : -1));

    // remove the 10 movies from store
    this.movieStore = this.movieStore.filter(
      (movie) => !this.cards.includes(movie)
    );
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
