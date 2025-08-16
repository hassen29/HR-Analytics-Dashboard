from django.db import models

class AttritionPrediction(models.Model):
    age = models.IntegerField(null=True, blank=True)
    daily_rate = models.FloatField(null=True, blank=True)
    distance_from_home = models.FloatField(null=True, blank=True)
    monthly_income = models.FloatField(null=True, blank=True)
    overtime = models.CharField(max_length=10, null=True, blank=True)  # Yes/No

    prediction = models.IntegerField()  # 0 or 1
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction: {self.prediction} (Age: {self.age})"
