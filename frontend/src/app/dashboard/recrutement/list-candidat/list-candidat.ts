import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Recrutement } from '../../../services/recrutement';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-list-candidat',
  imports: [FormsModule, CommonModule],
 
  templateUrl: './list-candidat.html',
  styleUrls: ['./list-candidat.css']  // plural
})
export class ListCandidat implements OnInit {
  candidates: any
  predictions: any

  constructor(private predictionservice: Recrutement) {}

  ngOnInit(): void {
    // Charger les candidats
    this.predictionservice.getcandidat().subscribe({
      next: (res) => {
        this.candidates = res;
        console.log('Candidates:', this.candidates);
      },
      error: (err) => {
        console.error('Error fetching candidates:', err);
      }
    });

    // Charger les prédictions
    this.predictionservice.getpredictions().subscribe({
      next: (data) => {
        this.predictions = data;
        console.log('Predictions:', data);
      },
      error: (err) => {
        console.error('Erreur de récupération:', err);
      }
    });
  }
}
