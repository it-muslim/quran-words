import { Surah, SurahMain, Ayah } from './quran.model';

describe('Ayah', () => {
  it('should create an instance', () => {
    expect(new Ayah()).toBeTruthy();
  });
});

describe('Surah', () => {
  it('should create an instance', () => {
    expect(new Surah()).toBeTruthy();
  });
});

describe('SurahMain', () => {
  it('should create an instance', () => {
    expect(new SurahMain()).toBeTruthy();
  });
});
