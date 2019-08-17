import { Component, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';
import { ActivatedRoute, Router } from '@angular/router';
import { RestService } from 'src/app/_services/rest.service';
import { SurahMain } from 'src/app/_models/quran.model';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})

export class HomeComponent implements OnInit {

  env = environment;
  surahs: Array<SurahMain>;
  selectedReciterId = 1;
  selectedSurahNumber = 1;

  constructor(public rest: RestService, private route: ActivatedRoute, private router: Router) { }

  ngOnInit() {
  }

  trackByFn(index, item) {
    return index;
  }
}
