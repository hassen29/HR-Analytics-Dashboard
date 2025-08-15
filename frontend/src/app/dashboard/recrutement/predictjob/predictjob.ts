import { Component } from '@angular/core';
import { Recrutement } from '../../../services/recrutement';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-predictjob',
  templateUrl: './predictjob.html',
  styleUrls: ['./predictjob.css'],
  imports: [FormsModule, CommonModule]
})
export class Predictjob {
  selectedFiles: File[] = [];
  jobDescription: string = '';

  constructor(private service: Recrutement, private router: Router) {}

onFilesSelected(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    // Append new files to the existing list
    this.selectedFiles = [...this.selectedFiles, ...Array.from(input.files)];
  }

  // Optional: remove duplicates by filename
  this.selectedFiles = this.selectedFiles.filter((file, index, self) =>
    index === self.findIndex(f => f.name === file.name)
  );
}



  // ✅ Remove a file from the list
  removeFile(index: number) {
    this.selectedFiles.splice(index, 1);
  }

  uploadAndPredict() {
    if (!this.selectedFiles.length || !this.jobDescription) {
      alert("Please select CVs and enter a job description.");
      return;
    }

    const formData = new FormData();
    this.selectedFiles.forEach(file => {
      formData.append('cvs', file); // keep the same key for multiple files
    });
    formData.append('job_description', this.jobDescription);

    this.service.predictAndAdd(formData).subscribe({
      next: (res) => {
        console.log("Prediction results:", res);
        alert("Predictions completed successfully!");
        this.router.navigate(['/dashboard/recrutement/list']);
      },
      error: (err) => {
        console.error("Upload error", err);
        alert("Error uploading CVs.");
      }
    });
  }
}
