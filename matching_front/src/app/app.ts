import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Matching } from './matching/matching/matching';

@Component({
  selector: 'app-root',
  imports: [Matching],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('matching_front');
}
