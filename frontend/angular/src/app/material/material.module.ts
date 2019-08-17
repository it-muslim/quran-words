import { NgModule } from '@angular/core';
import {
  MatButtonModule, MatIconModule, MatToolbarModule, MatSelectModule,
  MatFormFieldModule, MatCardModule, MatGridListModule, MatSidenavModule, MatListModule, MatInputModule, MatSliderModule
} from '@angular/material';

const material = [
  MatButtonModule,
  MatIconModule,
  MatToolbarModule,
  MatSelectModule,
  MatFormFieldModule,
  MatCardModule,
  MatGridListModule,
  MatSidenavModule,
  MatListModule,
  MatInputModule,
  MatSliderModule,
];

@NgModule({
  declarations: [],
  imports: [material],
  exports: [material]
})
export class MaterialModule { }
