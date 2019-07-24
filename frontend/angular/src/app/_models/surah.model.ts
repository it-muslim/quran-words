import { Ayah } from './ayah.model';

export class Surah {
    number: number;
    ayahs: Array<Ayah>;
    name: string;
    total_ayahs: number;
}

export class SurahMain {
    number: number;
    name: string;
    total_ayahs: number;
}
