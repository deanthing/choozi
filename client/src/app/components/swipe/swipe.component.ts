import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api/api.service';
import { StateService } from 'src/app/services/state/state.service';
import { IGroup, IMovie } from 'src/models/userData';

@Component({
  selector: 'app-swipe',
  templateUrl: './swipe.component.html',
  styleUrls: ['./swipe.component.css'],
})
export class SwipeComponent implements OnInit {
  cards: IMovie[] = [];

  constructor(
    private apiService: ApiService,
    private stateService: StateService
  ) {
    // gen movies
    // this.apiService
    //   .getData('moviegen', this.stateService.group!.id)
    //   .subscribe(() => console.log('movies generated'));
    this.apiService.getData('groups', 3).subscribe((group: IGroup) => {
      console.log(group.movies!.slice(0, 9));
      this.cards = group
        .movies!.slice(0, 9)
        .sort(() => (Math.random() > 0.5 ? 1 : -1));
    });
    // this.cards = [
    //   {
    //     img: 'https://placeimg.com/300/300/people',
    //     title: 'Demo card 1',
    //     description: 'This is a demo for Tinder like swipe cards',
    //   },
    //   {
    //     img: 'https://placeimg.com/300/300/animals',
    //     title: 'Demo card 2',
    //     description: 'This is a demo for Tinder like swipe cards',
    //   },
    //   {
    //     img: 'https://placeimg.com/300/300/nature',
    //     title: 'Demo card 3',
    //     description: 'This is a demo for Tinder like swipe cards',
    //   },
    //   {
    //     img: 'https://placeimg.com/300/300/tech',
    //     title: 'Demo card 4',
    //     description: 'This is a demo for Tinder like swipe cards',
    //   },
    //   {
    //     img: 'https://placeimg.com/300/300/arch',
    //     title: 'Demo card 5',
    //     description: 'This is a demo for Tinder like swipe cards',
    //   },
    // ];
  }

  ngOnInit(): void {}
}
