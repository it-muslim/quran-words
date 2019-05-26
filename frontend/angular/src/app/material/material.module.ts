import { NgModule } from '@angular/core';
import { MatToolbarModule, MatButtonModule, MatSidenavModule, MatIconModule, MatListModule } from '@angular/material';

const MaterialComponents = [
  MatToolbarModule,
  MatButtonModule,
  MatSidenavModule,
  MatIconModule,
  MatListModule,
]
@NgModule({
  declarations: [],
  imports: [
    MaterialComponents,
  ],
  exports: [
    MaterialComponents,
  ]
})
export class MaterialModule { }
