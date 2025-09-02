import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Turnover } from '../../../services/turnover';

@Component({
  selector: 'app-list',
  standalone: true, // ✅ required for imports
  imports: [RouterLink, CommonModule],
  templateUrl: './list.html',
  styleUrls: ['./list.css'] // ✅ plural
})
export class List implements OnInit {

  Attritions: any
  constructor(private attritionservice: Turnover) {}

  ngOnInit(): void {
    this.attritionservice.getAttrition().subscribe({
      next: (data) => {
        this.Attritions = data;
        console.log('Predictions:', data);
      },
      error: (err) => {
        console.error('Erreur de récupération:', err);
      }
    });
  }
}
