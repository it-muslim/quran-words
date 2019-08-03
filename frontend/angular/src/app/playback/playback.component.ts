import { Component, OnInit } from '@angular/core';
import { RestService } from 'src/app/_services/rest.service';
import { ActivatedRoute, Router, ParamMap } from '@angular/router';
import { Recitation } from '../_models/recite.model';
import { Surah, Ayah } from '../_models/quran.model';


@Component({
  selector: 'app-playback',
  templateUrl: './playback.component.html',
  styleUrls: ['./playback.component.scss']
})

export class PlaybackComponent implements OnInit {

  constructor(public rest: RestService, private route: ActivatedRoute, private router: Router) { }

  surahRecitation: Array<Recitation>;
  surah: Surah;
  currentAyah: Ayah;

  ngOnInit() {
    const surahNumber = +this.route.snapshot.paramMap.get('surahNumber') || 1;
    const reciterId = +this.route.snapshot.paramMap.get('reciterId') || 1;

    this.getRecitations(surahNumber, reciterId);
    this.getAyahs(surahNumber);

  }

  getRecitations(surahNumber: number, reciterId: number) {
    this.rest.getRecitations(surahNumber, reciterId)
      .subscribe((result: Array<Recitation>) => {
        this.surahRecitation = result;
      },
        (error: any) => {
          console.log('error', error);
        });
  }

  getAyahs(surahNumber: number) {
    this.rest.getSurah(surahNumber)
      .subscribe((result: Surah) => {
        this.surah = result;
        console.log(this.surah.ayahs);
      },
        (error: any) => {
          console.log('error', error);
        });
  }

  playAyahs() {
    let delay = 0;

    this.surah.ayahs.forEach((ayah: Ayah) => {
      setTimeout(() => {
        this.currentAyah = ayah;
      }, delay);

      const duration = this.surahRecitation
        .find(recitation => {
          return recitation.ayah === ayah.number;
        }).duration;
      delay += duration;
    });
  }

}
