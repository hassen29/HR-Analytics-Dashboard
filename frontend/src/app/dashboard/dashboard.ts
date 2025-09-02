import { Component } from '@angular/core';
import { Footer } from "./layout/footer/footer";
import { Header } from "./layout/header/header";
import { Sidebar } from "./layout/sidebar/sidebar";
import { RouterOutlet } from '@angular/router';
import { Powerbi } from "./powerbi/powerbi";

@Component({
  selector: 'app-dashboard',
  imports: [Footer, Header, Sidebar, RouterOutlet],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard {

}
