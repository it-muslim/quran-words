import { Component, HostListener } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})

export class NavbarComponent{
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
}
