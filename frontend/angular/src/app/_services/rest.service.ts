import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError, BehaviorSubject } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Reciter, Recitation } from 'src/app/_models/recite.model';
import { SurahMain, Surah } from 'src/app/_models/quran.model';
import { map, catchError } from 'rxjs/operators';


const endpoint = environment.api_url;

@Injectable({
  providedIn: 'root'
})

export class RestService {
  reciters$: BehaviorSubject<Array<Reciter>> = new BehaviorSubject<Array<Reciter>>([]);
  surahs$: BehaviorSubject<Array<SurahMain>> = new BehaviorSubject<Array<SurahMain>>([]);

  constructor(private http: HttpClient) {
    this.getReciters();
    this.getSurahs();
   }

  getReciters(): Observable<Array<Reciter>> {
    const fetch$: Observable<Array<Reciter>> = this.http.get<Array<Reciter>>(`${endpoint}reciters/`);
    fetch$
      .pipe(map(data => data.map(reciterData => new Reciter().deserialize(reciterData))))
      .subscribe((result: Array<Reciter>) => {
        this.reciters$.next(result);
      },
      (error: any) => {
        console.log('error', error);
      });
    return fetch$;
  }

  getSurahs(): Observable<Array<SurahMain>> {
    const fetch$: Observable<Array<SurahMain>> = this.http.get<Array<SurahMain>>(`${endpoint}surahs/`);
    fetch$
      .pipe(map(data => data.map(surahData => new SurahMain().deserialize(surahData))))
      .subscribe((result: Array<SurahMain>) => {
        this.surahs$.next(result);
      },
      (error: any) => {
        console.log('error', error);
      });
    return fetch$;
  }

  getSurah(surahNumber: number): Observable<Surah> {
    return this.http.get<Surah>(`${endpoint}surahs/${surahNumber}`)
    .pipe(map(data => new Surah().deserialize(data)),
      catchError(() => throwError('Surah not found')));
  }

  getRecitations(surahNumber: number, reciterId: number): Observable<Array<Recitation>> {
    return this.http.get<Array<Recitation>>(`${endpoint}recitations/?reciter_id=${reciterId}&surah_number=${surahNumber}`)
      .pipe(map(data => data.map(recitationData => new Recitation().deserialize(recitationData))));
  }
}
