import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth';
import { SafeUrlPipe } from '../../safe-url-pipe';

@Component({
  selector: 'app-powerbi',
  imports: [ SafeUrlPipe],
  templateUrl: './powerbi.html',
  styleUrl: './powerbi.css'
})
export class Powerbi implements OnInit {

  reportUrl: string = '';

  // Replace these with your actual Power BI embed links
  employeeReport = "https://app.powerbi.com/reportEmbed?reportId=f38d1557-fe80-4fca-9989-f58e670bea64&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730";
  hrReport = "https://app.powerbi.com/reportEmbed?reportId=141286a4-c4a5-459d-b399-c16e8a4668b5&autoAuth=true&ctid=604f1a96-cbe8-43f8-abbf-f8eaf5d85730";

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    const role = this.authService.getUserRole();
    if (role === 'admin') {
      this.reportUrl = this.hrReport;
    } else {
      this.reportUrl = this.employeeReport;
    }
  }
}