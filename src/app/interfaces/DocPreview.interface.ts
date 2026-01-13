import { SafeResourceUrl } from '@angular/platform-browser';

export interface DocPreview {
  name: string;
  type: string;
  rawUrl: string;
  safeUrl: SafeResourceUrl;
  isPdf: boolean;
}

