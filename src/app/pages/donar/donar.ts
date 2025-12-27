import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../../shared/header/header';
import { FooterComponent } from '../../shared/footer/footer';
import { RouterModule } from '@angular/router';
import { ChatbotIaComponent } from '../../shared/chatbot-ia/chatbot-ia.component';

@Component({
  selector: 'app-donar',
  standalone: true,
  imports: [CommonModule, HeaderComponent, FooterComponent, RouterModule, ChatbotIaComponent],
  templateUrl: './donar.html',
  styleUrls: ['./donar.scss']
})
export class DonarComponent {}
