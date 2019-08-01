import { Recitation } from './recite.model';
import { Reciter } from './recite.model';

describe('Recitation', () => {
  it('should create an instance', () => {
    expect(new Recitation()).toBeTruthy();
  });
});

describe('Reciter', () => {
  it('should create an instance', () => {
    expect(new Reciter()).toBeTruthy();
  });
});
