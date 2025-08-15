import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Recrutement } from '../../../services/recrutement';

@Component({
  selector: 'app-list-candidat',
  imports: [RouterLink],
  templateUrl: './list-candidat.html',
  styleUrls: ['./list-candidat.css']  // plural
})
export class ListCandidat implements OnInit {
  candidates: any;

  constructor(private __cand: Recrutement) {}

  ngOnInit(): void {
    this.__cand.getcandidat()
      .subscribe(
        (res) => {
          this.candidates = res;
          console.log('Candidates:', this.candidates); 
        },
        (err) => {
          console.error('Error fetching candidates:', err);
        }
      );
  }
}
