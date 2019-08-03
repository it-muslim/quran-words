import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NavbarComponent } from './navbar/navbar.component';
import { HomeComponent } from './home/home.component';
import { LayoutModule } from '@angular/cdk/layout';
import { MaterialModule } from './material/material.module';
import { HttpClientModule } from '@angular/common/http';
import { PlaybackComponent } from './playback/playback.component';
import { FormsModule } from '@angular/forms';
import { RestService } from './_services/rest.service';
import { RecitationsResolver } from './_resolvers/recitations.resolver';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    HomeComponent,
    PlaybackComponent,
  ],
  imports: [
    MaterialModule,
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    LayoutModule,
    HttpClientModule,
    FormsModule,
  ],
  providers: [RestService, RecitationsResolver],
  bootstrap: [AppComponent]
})
export class AppModule { }
