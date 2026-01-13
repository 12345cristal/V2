import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

export interface Notification {
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  duration?: number;
}

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private notificationSubject = new Subject<Notification>();
  notification$ = this.notificationSubject.asObservable();

  success(message: string, duration = 3000): void {
    this.notificationSubject.next({ message, type: 'success', duration });
  }

  error(message: string, duration = 4000): void {
    this.notificationSubject.next({ message, type: 'error', duration });
  }

  info(message: string, duration = 3000): void {
    this.notificationSubject.next({ message, type: 'info', duration });
  }

  warning(message: string, duration = 3000): void {
    this.notificationSubject.next({ message, type: 'warning', duration });
  }
}




