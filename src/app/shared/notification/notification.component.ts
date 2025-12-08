import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { Subscription } from 'rxjs';

import { NotificationService, Notification } from '../notification.service';

@Component({
  selector: 'app-notification',
  standalone: true,
  imports: [CommonModule, MatIconModule],
  templateUrl: './notification.component.html',
  styleUrls: ['./notification.component.scss']
})
export class NotificationComponent implements OnInit, OnDestroy {
  currentNotification: Notification | null = null;
  private subscription?: Subscription;
  private timeoutId?: number;

  constructor(private notificationService: NotificationService) {}

  ngOnInit(): void {
    this.subscription = this.notificationService.notification$.subscribe(
      notification => {
        this.currentNotification = notification;
        
        if (this.timeoutId) {
          clearTimeout(this.timeoutId);
        }

        this.timeoutId = window.setTimeout(() => {
          this.close();
        }, notification.duration || 3000);
      }
    );
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
    }
  }

  close(): void {
    this.currentNotification = null;
  }
}
