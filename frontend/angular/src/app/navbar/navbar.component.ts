import { Component, HostListener, ViewChild } from '@angular/core';
import { SidenavService } from '../_services/sidenav.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})

export class NavbarComponent{

  constructor(private sidenav: SidenavService) { }

  sidenavOpen = false;
  showNavbar = true;

  @HostListener('body:mouseleave', ['$event'])
  MouseLeaveTop(event: MouseEvent) {
    if (event.clientY <= 0) {
      this.showNavbar = true;
    }
  }

  @HostListener('body:mouseenter', ['$event'])
  MouseBack(event: MouseEvent) {
    this.showNavbar = false;
  }

  toggleLeftSidenav() {
    this.sidenavOpen = !this.sidenavOpen;
    this.sidenav.toggle();
    this.sidenavOpen ? this.showNavbar = true : this.showNavbar = false;
  }
}
