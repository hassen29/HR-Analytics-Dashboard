from django.db import models

# Create your models here.

class Candidate(models.Model):
    name = models.CharField(max_length=100)  # fixed
    email = models.EmailField(null=True, blank=True)
    uploaded_cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    predicted_job = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


  

class JobPrediction(models.Model):
    cv_file = models.FileField(upload_to='cv_file/', null=True, blank=True)
    predicted_role = models.CharField(max_length=255)

    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    university = models.CharField(max_length=255, null=True, blank=True)
  
    skills = models.TextField(null=True, blank=True)
    langues = models.TextField(null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    job_description = models.TextField(null=True, blank=True)
    fit_score = models.FloatField(null=True, blank=True)
    matched_skills = models.TextField(null=True, blank=True)
    missing_skills = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.predicted_role} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"

  







