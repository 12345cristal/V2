import { Component } from '@angular/core';
import { FooterComponent } from "../../shared/footer/footer";
import { HeaderComponent } from "../../shared/header/header";

@Component({
  selector: 'app-servicios',
  templateUrl: './servicios.html',
  styleUrls: ['./servicios.scss'],
  imports: [FooterComponent, HeaderComponent]
})
export class ServiciosComponent {}
