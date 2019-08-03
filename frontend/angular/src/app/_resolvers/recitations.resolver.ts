import { Injectable } from '@angular/core';
import { Resolve, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { RestService } from '../_services/rest.service';
import { Observable } from 'rxjs';
import { SurahWithRecitations } from '../_models/quran.model';

@Injectable()
export class RecitationsResolver implements Resolve<SurahWithRecitations> {
    constructor(private rest: RestService) { }
    resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<SurahWithRecitations> {
        const surahNumber = +route.paramMap.get('surahNumber') || 1;
        const reciterId = +route.paramMap.get('reciterId') || 1;

        return this.rest.getAyahRecitations(surahNumber, reciterId);
    }
}
