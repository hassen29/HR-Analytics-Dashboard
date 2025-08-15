from rest_framework.serializers import ModelSerializer
from .models import *

class CandiateSerializer(ModelSerializer):
    class Meta : 
        model = Candidate
        fields = '__all__'




class JobPredictionSerializer(ModelSerializer):
    class Meta:
        model = JobPrediction
        fields = '__all__'


