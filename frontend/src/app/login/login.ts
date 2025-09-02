



import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../services/auth';

@Component({
  selector: 'app-login',
  
  imports : [RouterLink, FormsModule, CommonModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {
  email = '';
  password = '';
  errorMessage = '';

  constructor(private authService: AuthService, private router: Router) { }

  onSubmit() {
    const credentials = { email: this.email, password: this.password };

    this.authService.login(credentials).subscribe(
      response => {
        // Handle successful login
        console.log('Login successful:', response);
        this.router.navigate(['/dashboard']);
      },
      error => {
        // Handle login error
        console.error('Login failed:', error);
        this.errorMessage = 'Invalid email or password. Please try again.';
      }
    );
  }
}
