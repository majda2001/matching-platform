import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class MatchingService {
  
private apiUrl = 'http://localhost:8080/api/match/resume-job';

  constructor(private http: HttpClient) { }

  getMatchResult(file: File, jobText: string): Observable<any> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('jobText', jobText);

  return this.http.post<any>(this.apiUrl, formData);
}

}