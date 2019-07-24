import { Component, OnInit } from '@angular/core';
import { RestService } from 'src/app/_services/rest.service';
import { ActivatedRoute, Router, ParamMap } from '@angular/router';
import { Recitation } from '../_models/recitation.model';
import { Surah } from '../_models/surah.model';
import { Ayah } from '../_models/ayah.model';


@Component({
  selector: 'app-playback',
  templateUrl: './playback.component.html',
  styleUrls: ['./playback.component.scss']
})

export class PlaybackComponent implements OnInit {

  constructor(public rest:RestService, private route: ActivatedRoute, private router: Router) { }

  surahRecitation: Array<Recitation>;
  surah: Surah;
  ayahs: Array<Ayah>;

  ngOnInit() {
    let surahNumber = +this.route.snapshot.paramMap.get('surahNumber') || 1;
    let reciterId = +this.route.snapshot.paramMap.get('reciterId') || 1;
    this.getRecitations(surahNumber, reciterId);
    this.getAyahs(surahNumber);
  }

  getRecitations(surahNumber: number, reciterId: number) {
    this.rest.getRecitations(surahNumber, reciterId)
      .subscribe((result: Array<Recitation>) => {
        this.surahRecitation = result}),
        (error: any) => {
          console.log('error', error);
        }
  }

  getAyahs(surahNumber: number) {
    this.rest.getSurah(surahNumber)
      .subscribe((result: Surah) => {
        this.surah = result
        this.ayahs = this.surah.ayahs
      }),
        (error: any) => {
          console.log('error', error);
        }
  }
}
