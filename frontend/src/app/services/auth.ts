import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private userSubject = new BehaviorSubject<string | null>(null);
  user$ = this.userSubject.asObservable();

  private apiUrl = 'http://127.0.0.1:8000/api';  // Django backend URL

  constructor(private http: HttpClient) {}

  // Register new user
  register(userData: { username: string; email: string; password1: string; password2: string; role: string }): Observable<any> {
    return this.http.post(`${this.apiUrl}/register/`, userData);
  }

  // Login user
  login(credentials: { email: string; password: string }): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login/`, credentials).pipe(
      tap(response => {
        localStorage.setItem('access_token', response.tokens.access);
        localStorage.setItem('refresh_token', response.tokens.refresh);
        localStorage.setItem('user_role', response.role);
        this.userSubject.next(response.username);
      })
    );
  }

  // Logout user
  logout(): Observable<any> {
    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
      return of({ error: 'No token found' });
    }

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    });

    return this.http.post(`${this.apiUrl}/logout/`, {}, { headers }).pipe(
      tap(() => {
        // Clear tokens and user state
        localStorage.clear();
        this.userSubject.next(null);
      })
    );
  }

  // Helper: Get current username
  getUsername(): Observable<string | null> {
    return this.user$;
  }

  // Helper: Check if user is logged in
  isLoggedIn(): boolean {
    return !!localStorage.getItem('access_token');
  }

  // Helper: Get access token
  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

    getUserRole(): string | null {
    return localStorage.getItem('user_role');
  }
}
