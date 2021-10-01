import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
@Component({
  selector: 'app-name',
  templateUrl: './name.component.html',
  styleUrls: ['./name.component.css'],
})
export class NameComponent implements OnInit {
  form = new FormGroup({
    name: new FormControl(''),
  });

  constructor(private router: Router) {}

  ngOnInit(): void {}

  onStart() {
    console.log(this.form.value);
    this.router.navigateByUrl('/waitingroom');
  }
}
