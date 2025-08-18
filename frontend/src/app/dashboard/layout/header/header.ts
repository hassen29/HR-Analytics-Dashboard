import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../services/auth';


@Component({
  selector: 'app-header',
  imports : [FormsModule, CommonModule],
  templateUrl: './header.html',
  styleUrls: ['./header.css']
})
export class Header {
  username: string | null = null;

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    // Subscribe to the username from the service
    this.authService.getUsername().subscribe(username => {
      this.username = username;
    });
  }

  onLogout(): void {
    this.authService.logout().subscribe(
      () => {
        // Redirect to login after logout
        this.router.navigate(['/login']);
      },
      error => {
        console.error('Logout error:', error);
        // Even if logout fails, clear localStorage and redirect
        localStorage.clear();
        this.router.navigate(['/login']);
      }
    );
  }
}
