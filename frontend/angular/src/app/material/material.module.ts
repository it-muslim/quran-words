import { NgModule } from '@angular/core';
import { MatButtonModule, MatIconModule, MatToolbarModule, MatSelectModule,
  MatFormFieldModule, MatCardModule, MatGridListModule, MatSidenavModule, MatListModule } from '@angular/material';

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
];

@NgModule({
  declarations: [],
  imports: [material],
  exports: [material]
})
export class MaterialModule { }
