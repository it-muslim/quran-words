import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { environment } from 'src/environments/environment'; 
import { Reciter } from "src/app/_models/reciter.model";
import { SurahMain, Surah } from "src/app/_models/surah.model";
import { Recitation } from "src/app/_models/recitation.model";


const endpoint = environment.api_url;

@Injectable({
  providedIn: 'root'
})

export class RestService {
  constructor(private http: HttpClient) { }

  getReciters(): Observable<Array<Reciter>> {
    return this.http.get<Array<Reciter>>(`${endpoint}reciters/`);
  }

  getSurahs(): Observable<Array<SurahMain>> {
    return this.http.get<Array<SurahMain>>(`${endpoint}surahs/`);
  }

  getSurah(number: number): Observable<Surah> {
    return this.http.get<Surah>(`${endpoint}surahs/${number}`);
  }

  getRecitations(reciterId: number, surahNumber: number): Observable<Array<Recitation>> {
    return this.http.get<Array<Recitation>>(`${endpoint}recitations/?reciter_id=${reciterId}&surah_number=${surahNumber}`);
  }
 }
