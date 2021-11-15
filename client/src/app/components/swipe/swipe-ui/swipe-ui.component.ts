import {
  Component,
  Input,
  ViewChildren,
  QueryList,
  ElementRef,
  Renderer2,
  Output,
  EventEmitter,
} from '@angular/core';
import { IMovie } from 'src/models/userData';

interface ICard {
  img: string;
  title: string;
  description: string;
}

@Component({
  selector: 'app-swipe-ui',
  templateUrl: './swipe-ui.component.html',
  styleUrls: ['./swipe-ui.component.css'],
})
export class SwipeUiComponent {
  @Input('cards') cards!: Array<IMovie>;

  @Output() choiceMade = new EventEmitter();

  @ViewChildren('tinderCard') tinderCards!: QueryList<ElementRef>;
  tinderCardsArray: Array<ElementRef> = [];

  moveOutWidth: number; // value in pixels that a card needs to travel to dissapear from screen
  shiftRequired: boolean; // state variable that indicates we need to remove the top card of the stack
  transitionInProgress: boolean; // state variable that indicates currently there is transition on-going
  heartVisible: boolean;
  crossVisible: boolean;
  imageBase: string = 'https://image.tmdb.org/t/p/w400';

  mousePosition = {
    x: 0,
    y: 0,
  };

  showDetail: boolean;
  constructor(private renderer: Renderer2) {
    this.moveOutWidth = document.documentElement.clientWidth * 1.5;
    this.shiftRequired =
      this.transitionInProgress =
      this.heartVisible =
      this.crossVisible =
      this.showDetail =
        false;
  }

  cardClick($event: any) {
    if (
      this.mousePosition.x === $event.screenX &&
      this.mousePosition.y === $event.screenY
    ) {
      this.showDetail = !this.showDetail;
    }
  }

  mouseDown($event: any) {
    this.mousePosition.x = $event.screenX;
    this.mousePosition.y = $event.screenY;
  }

  userClickedButton(event: any, heart: boolean) {
    event.preventDefault();
    if (!this.cards.length) return;
    if (heart) {
      this.renderer.setStyle(
        this.tinderCardsArray[0].nativeElement,
        'transform',
        'translate(' + this.moveOutWidth + 'px, -100px) rotate(-30deg)'
      );
      this.toggleChoiceIndicator(false, true);
      this.emitChoice(heart, this.cards[0]);
    } else {
      this.renderer.setStyle(
        this.tinderCardsArray[0].nativeElement,
        'transform',
        'translate(-' + this.moveOutWidth + 'px, -100px) rotate(30deg)'
      );
      this.toggleChoiceIndicator(true, false);
      this.emitChoice(heart, this.cards[0]);
    }
    this.shiftRequired = true;
    this.transitionInProgress = true;
  }

  handlePan(event: any) {
    if (
      event.deltaX === 0 ||
      (event.center.x === 0 && event.center.y === 0) ||
      !this.cards.length
    )
      return;

    this.renderer.addClass(this.tinderCardsArray[0].nativeElement, 'moving');

    if (event.deltaX > 0) {
      this.toggleChoiceIndicator(false, true);
    }
    if (event.deltaX < 0) {
      this.toggleChoiceIndicator(true, false);
    }

    let xMulti = event.deltaX * 0.03;
    let yMulti = event.deltaY / 80;
    let rotate = xMulti * yMulti;

    this.renderer.setStyle(
      this.tinderCardsArray[0].nativeElement,
      'transform',
      'translate(' +
        event.deltaX +
        'px, ' +
        event.deltaY +
        'px) rotate(' +
        rotate +
        'deg)'
    );

    // this.shiftRequired = true;
  }

  handlePanEnd(event: any) {
    this.toggleChoiceIndicator(false, false);

    if (!this.cards.length) return;

    this.renderer.removeClass(this.tinderCardsArray[0].nativeElement, 'moving');

    let keep = Math.abs(event.deltaX) < 80;

    if (keep) {
      this.renderer.setStyle(
        this.tinderCardsArray[0].nativeElement,
        'transform',
        ''
      );
      this.shiftRequired = false;
    } else {
      let endX = Math.max(
        Math.abs(event.velocityX) * this.moveOutWidth,
        this.moveOutWidth
      );
      let toX = event.deltaX > 0 ? endX : -endX;
      let endY = Math.abs(event.velocityY) * this.moveOutWidth;
      let toY = event.deltaY > 0 ? endY : -endY;
      let xMulti = event.deltaX * 0.03;
      let yMulti = event.deltaY / 80;
      let rotate = xMulti * yMulti;

      this.renderer.setStyle(
        this.tinderCardsArray[0].nativeElement,
        'transform',
        'translate(' +
          toX +
          'px, ' +
          (toY + event.deltaY) +
          'px) rotate(' +
          rotate +
          'deg)'
      );

      this.shiftRequired = true;

      this.emitChoice(!!(event.deltaX > 0), this.cards[0]);
    }
    // this.transitionInProgress = true;
    this.showDetail = false;
  }

  toggleChoiceIndicator(cross: boolean, heart: boolean) {
    this.crossVisible = cross;
    this.heartVisible = heart;
  }

  handleShift() {
    this.transitionInProgress = false;
    this.toggleChoiceIndicator(false, false);
    if (this.shiftRequired) {
      this.shiftRequired = false;
      this.cards.shift();
    }
  }

  emitChoice(heart: boolean, card: IMovie) {
    this.choiceMade.emit({
      choice: heart,
      payload: card,
    });
  }

  ngAfterViewInit() {
    this.moveOutWidth = document.documentElement.clientWidth * 1.5;
    this.tinderCardsArray = this.tinderCards.toArray();
    this.tinderCards.changes.subscribe(() => {
      this.tinderCardsArray = this.tinderCards.toArray();
    });
  }
}
