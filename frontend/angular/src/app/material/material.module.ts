import { NgModule } from '@angular/core';
import { MatButtonModule, MatIconModule, MatToolbarModule, MatSelectModule,
  MatFormFieldModule, MatCardModule, MatGridListModule } from '@angular/material';

const material = [
  MatButtonModule,
  MatIconModule,
  MatToolbarModule,
  MatSelectModule,
  MatFormFieldModule,
  MatCardModule,
  MatGridListModule,
];

@NgModule({
  declarations: [],
  imports: [material],
  exports: [material]
})
export class MaterialModule { }
