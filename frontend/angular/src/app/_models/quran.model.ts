import { Deserializable } from './deserializable.model';


export class SurahMain {
    number: number;
    name: string;
    total_ayahs: number;

    deserialize(input: any): this {
        return Object.assign(this, input);
    }
}

export class Ayah {
    number: number;
    text: string;

    deserialize(input: any): this {
        return Object.assign(this, input);
    }
}

export class Surah implements Deserializable {
    number: number;
    ayahs: Array<Ayah>;
    name: string;
    total_ayahs: number;

    deserialize(input: any): this {
        Object.assign(this, input);

        this.ayahs = input.ayahs.map(ayah => {
            new Ayah().deserialize(ayah);
        });
        return this;
    }
}
