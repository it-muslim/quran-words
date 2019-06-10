import { Component, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';
import { ActivatedRoute, Router } from '@angular/router';
import { RestService } from 'src/app/_services/rest.service';
import { Reciter } from 'src/app/_models/reciter';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  
  title = 'angular';
  env = environment;
  reciters: Array<Reciter>;

  constructor(public rest:RestService, private route: ActivatedRoute, private router: Router) { }

  ngOnInit() {
    this.showReciters();
  }

  showReciters() {
    this.rest.getReciters()
      .subscribe((result: Array<Reciter>) => {
        this.reciters = result}),
        (error: any) => {
          console.log('error', error);
        }
  }
}
