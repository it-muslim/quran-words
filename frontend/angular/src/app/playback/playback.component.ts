import { Component, OnInit, OnDestroy } from '@angular/core';
import { RestService } from 'src/app/_services/rest.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Ayah, SurahWithRecitations } from '../_models/quran.model';
import { trigger, state, style, animate, transition } from '@angular/animations';
import { ThemeService } from '../_services/theme.service';


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

  constructor(public rest: RestService, private route: ActivatedRoute, private router: Router, public themeService: ThemeService) { }

  stopped = false;
  surahRecitation: SurahWithRecitations;
  currentAyah: Ayah;
  currentWordIndex: number;
  theme = this.themeService.theme || null;

  ngOnInit() {
    this.surahRecitation = this.route.snapshot.data.recitations;
    this.playAyahs();
  }

  playAyahs() {
    if (!this.surahRecitation) {
      return false;
    }

    let delayAyah = 0;

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
        this.highLightWords(currentRecitation);
      }, delayAyah);

      delayAyah += currentRecitation.duration + 1;
    });
  }

  highLightWords(currentRecitation) {
    let delayWord = 0;

    for (let index = 0; index < currentRecitation.segments.length + 1; index++) {
      const segment = currentRecitation.segments[index];
      setTimeout(() => {
        if (this.stopped) {
          return false;
        }
        this.currentWordIndex = index;
      }, delayWord);

      if (segment) {
        delayWord += (segment[1] - segment[0]);
      }
    }
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
