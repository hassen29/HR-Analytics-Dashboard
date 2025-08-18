

import { Component } from '@angular/core';

import { Router } from '@angular/router';
import { AuthService } from '../services/auth';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-register',
    imports: [FormsModule,CommonModule],
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class Register {
  userData = {
    username: '',
    email: '',
    password1: '',
    password2: '',
    role: 'employee'  // Default role can be manager or admin
  };

  errorMessage: string = '';  // For error handling

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit() {
    if (this.userData.password1 !== this.userData.password2) {
      this.errorMessage = "Passwords do not match!";
      return;
    }

    this.authService.register(this.userData).subscribe(
      response => {
        console.log('Registration successful', response);
        this.router.navigate(['/login']);
      },
      error => {
        console.error('Registration failed', error);
        this.errorMessage = 'Registration failed. Please try again.';
      }
    );
  }}