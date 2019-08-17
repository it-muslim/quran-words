import { Component, OnInit } from '@angular/core';
import { ThemeService } from '../_services/theme.service';
import { Theme } from '../_models/theme.model';

@Component({
  selector: 'app-theme',
  templateUrl: './theme.component.html',
  styleUrls: ['./theme.component.scss']
})

export class ThemeComponent implements OnInit {
  constructor(private themeService: ThemeService) { }

  public theme = new Theme();

  ngOnInit(): void {
    this.themeService.setTheme(this.theme);
  }
}
