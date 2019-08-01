import { Deserializable } from './deserializable.model';

export class Recitation implements Deserializable {
    surah: number;
    ayah: number;
    segments: Array<Array<number>>;
    audio: string;
    reciter: number;
    duration: number;

    deserialize(input: any): this {
        Object.assign(this, input);
        this.duration = this.segments[this.segments.length - 1][1];
        return this;
    }
}

export class Reciter implements Deserializable {
    id: number;
    name: string;
    bitrate: number;
    style: string;
    slug: string;

    deserialize(input: any): this {
        return Object.assign(this, input);
    }
}
