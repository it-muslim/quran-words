import { Injectable } from '@angular/core';
import { Theme } from '../_models/theme.model';

@Injectable({
  providedIn: 'root'
})

export class ThemeService {
  public theme: Theme;

  public setTheme(theme: Theme) {
    this.theme = theme;
  }
}
