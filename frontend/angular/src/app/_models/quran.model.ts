import { Deserializable } from './deserializable.model';


export class Ayah {
    number: number;
    text: string;
    wordsArray: Array<string>;

    deserialize(input: any): this {
        Object.assign(this, input);
        this.wordsArray = input.text.split(',');
        return this;
    }
}

export class SurahMain {
    number: number;
    name: string;
    total_ayahs: number;

    deserialize(input: any): this {
        return Object.assign(this, input);
    }
}

export class Surah implements Deserializable {
    number: number;
    name: string;
    total_ayahs: number;
    ayahs: Array<Ayah>;

    deserialize(input: any): this {
        Object.assign(this, input);

        this.ayahs = input.ayahs
            .map((ayah: Ayah) => new Ayah().deserialize(ayah));
        return this;
    }
}
