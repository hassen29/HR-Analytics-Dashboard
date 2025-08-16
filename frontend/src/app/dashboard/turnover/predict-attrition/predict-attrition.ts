import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Turnover } from '../../../services/turnover';

@Component({
  selector: 'app-predict-attrition',
  imports: [FormsModule],
  templateUrl: './predict-attrition.html',
  styleUrl: './predict-attrition.css'
})
export class PredictAttrition {
  formData = {
    MonthlyIncome: null,
    Age: null,
    DailyRate: null,
    OverTime: null,
    DistanceFromHome: null
  };
  selectedFile: File | null = null;
  predictionResult: any = null;

  constructor(private service: Turnover, private router: Router) {}

  // Submit manual form
  submitForm() {
    this.service.predictAttrition(this.formData).subscribe({
      next: (res) => {
        if (res.type === "single") {
          this.predictionResult = res.prediction;
          alert(`Prediction (single): ${this.predictionResult}`);
        }
      },
      error: (err) => {
        console.error("Prediction error", err);
        alert("Error making prediction");
      }
    });
  }

  // Handle file selection
  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  // Upload CSV for bulk prediction
  uploadAndPredict() {
    if (!this.selectedFile) {
      alert("Please select a CSV file.");
      return;
    }

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.service.predictAttrition(formData).subscribe({
      next: (res) => {
        if (res.type === "csv") {
          console.log("Bulk prediction results:", res.predictions);
          alert(`Bulk predictions: ${res.predictions.join(', ')}`);
        }
        this.router.navigate(['/dashboard/attrition/list']);
      },
      error: (err) => {
        console.error("Upload error", err);
        alert("Error uploading CSV.");
      }
    });
  }
}
