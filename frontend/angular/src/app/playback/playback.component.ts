import { Component, OnInit } from '@angular/core';
import { RestService } from 'src/app/_services/rest.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Ayah, SurahWithRecitations } from '../_models/quran.model';


@Component({
  selector: 'app-playback',
  templateUrl: './playback.component.html',
  styleUrls: ['./playback.component.scss']
})

export class PlaybackComponent implements OnInit {

  constructor(public rest: RestService, private route: ActivatedRoute, private router: Router) { }

  surahRecitation: SurahWithRecitations;
  currentAyah: Ayah;

  ngOnInit() {
    this.surahRecitation = this.route.snapshot.data.recitations;
    this.playAyahs();
  }

  playAyahs() {
    let delay = 0;

    this.surahRecitation.surah.ayahs.forEach((ayah: Ayah) => {
      setTimeout(() => {
        this.currentAyah = ayah;
      }, delay);

      const duration = this.surahRecitation.recitations
        .find(recitation => {
          return recitation.ayah === ayah.number;
        }).duration;
      delay += duration;
    });
  }

}
