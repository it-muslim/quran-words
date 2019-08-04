import { Component, OnInit, OnDestroy } from '@angular/core';
import { RestService } from 'src/app/_services/rest.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Ayah, SurahWithRecitations } from '../_models/quran.model';
import { trigger, state, style, animate, transition } from '@angular/animations';


@Component({
  selector: 'app-playback',
  templateUrl: './playback.component.html',
  styleUrls: ['./playback.component.scss'],
  animations: [
    trigger('ayahChangeTrigger', [
      transition(':enter', [
        style({ opacity: 0 }),
        animate('.5s'),
      ]),
    ]),
  ]
})

export class PlaybackComponent implements OnInit, OnDestroy {

  constructor(public rest: RestService, private route: ActivatedRoute, private router: Router) { }

  stopped = false;
  surahRecitation: SurahWithRecitations;
  currentAyah: Ayah;

  ngOnInit() {
    this.surahRecitation = this.route.snapshot.data.recitations;
    this.playAyahs();
  }

  playAyahs() {
    let delay = 0;

    this.surahRecitation.surah.ayahs.forEach((ayah: Ayah) => {
      const currentRecitation = this.surahRecitation.recitations
        .find(recitation => {
          return recitation.ayah === ayah.number;
        });

      setTimeout(() => {
        if (this.stopped) {
          return false;
        }
        this.currentAyah = ayah;
        this.playAudio(currentRecitation.audio);
      }, delay);

      delay += currentRecitation.duration;

    });
  }

  playAudio(audioPath: string) {
    const audio = new Audio();
    audio.src = audioPath;
    audio.load();
    audio.play();
  }

  ngOnDestroy() {
    this.stopped = true;
  }
}
