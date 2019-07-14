import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { environment } from 'src/environments/environment'; 
import { Reciter } from "src/app/_models/reciter.model";
import { Surah } from "src/app/_models/surah.model";

const endpoint = environment.api_url;

@Injectable({
  providedIn: 'root'
})

export class RestService {
  constructor(private http: HttpClient) { }

  getReciters(): Observable<Array<Reciter>> {
    return this.http.get<Array<Reciter>>(`${endpoint}reciters/`);
  }

  getSurahs(): Observable<Array<Surah>> {
    return this.http.get<Array<Surah>>(`${endpoint}surahs/`);
  }
 }
