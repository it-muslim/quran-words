import { Component, ViewChild, OnInit } from '@angular/core';
import { environment } from '../environments/environment';
import { MatSidenav } from '@angular/material';
import { SidenavService } from './_services/sidenav.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent implements OnInit {

  constructor(private sidenavService: SidenavService) { }

  env = environment;

  @ViewChild('sidenav') public sidenav: MatSidenav;

  ngOnInit(): void {
    this.sidenavService.setSidenav(this.sidenav);
  }
}
