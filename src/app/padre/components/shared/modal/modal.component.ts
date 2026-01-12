import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-modal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss'],
})
export class ModalComponent {
  @Input() isOpen: boolean = false;
  @Input() title?: string;
  @Input() size: 'sm' | 'md' | 'lg' | 'xl' = 'md';
  @Input() showCloseButton: boolean = true;
  @Input() closeOnBackdropClick: boolean = true;
  
  @Output() close = new EventEmitter<void>();
  
  onClose() {
    this.close.emit();
  }
  
  onBackdropClick() {
    if (this.closeOnBackdropClick) {
      this.onClose();
    }
  }
  
  onContentClick(event: Event) {
    event.stopPropagation();
  }
}
