import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatchingService } from '../service/matching-service';


@Component({
  selector: 'app-matching',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './matching.html',
  styleUrl: './matching.scss',
})

export class  Matching {

  selectedFile: File | null = null;
  fileName: string | null = null;
  jobDescription: string = '';
  
  
  matchScore: number = 0;
  isAnalyzed: boolean = false;
  isLoading: boolean = false;

  constructor(private matchingService: MatchingService,private cdr: ChangeDetectorRef) {}

 
  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
      this.fileName = file.name;
      this.isAnalyzed = false; 
    }
  }

analyze(): void {
  if (!this.selectedFile || !this.jobDescription) {
    alert("Veuillez sélectionner un CV et coller une offre d'emploi.");
    return;
  }

  this.isAnalyzed = false; 
  this.isLoading = true;

  this.matchingService
    .getMatchResult(this.selectedFile, this.jobDescription)
    .subscribe({
      next: (response) => {
       
        this.matchScore = Number(response.percentage); 
        this.isLoading = false;
        this.isAnalyzed = true;

        this.cdr.markForCheck();
        this.cdr.detectChanges();
        
        console.log('Réponse backend:', response);
      },
      error: (err) => {
        console.error('Erreur API:', err);
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
}
  
  removeFile(): void {
    this.selectedFile = null;
    this.fileName = null;
    this.isAnalyzed = false;
   
    const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
    if (fileInput) fileInput.value = '';
  }

 
  recalculate(): void {
    this.isAnalyzed = false;
  }
}