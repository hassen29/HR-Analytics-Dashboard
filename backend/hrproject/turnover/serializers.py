from rest_framework.serializers import ModelSerializer
from .models import AttritionPrediction

class AttritionPredictionSerializer(ModelSerializer):
    class Meta:
        model = AttritionPrediction
        fields = "__all__"
