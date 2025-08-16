import os
import pickle
import pandas as pd
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AttritionPrediction

from .serializers import AttritionPredictionSerializer

# Load model
model_path = os.path.join(settings.BASE_DIR, 'turnover', 'MLAttrition')
rf_model = pickle.load(open(os.path.join(model_path, 'logistic_regression_model.pkl'), 'rb'))
import os
import pickle
import pandas as pd
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AttritionPrediction

# Load your model
model_path = os.path.join(settings.BASE_DIR, 'turnover', 'MLAttrition')
rf_model = pickle.load(open(os.path.join(model_path, 'logistic_regression_model.pkl'), 'rb'))

@api_view(['POST'])
def predictAttrition(request):
    print("Incoming predict request")

    # 1. CSV bulk prediction
    csv_file = request.FILES.get('file', None)
    if csv_file:
        try:
            df = pd.read_csv(csv_file)
            preds = rf_model.predict(df)

            # Save each prediction into DB with status
            records = []
            for i, row in df.iterrows():
                pred = int(preds[i])
                status_label = "Will Leave" if pred == 1 else "Will Stay"

                records.append(
                    AttritionPrediction(
                        age=row.get("Age"),
                        daily_rate=row.get("DailyRate"),
                        distance_from_home=row.get("DistanceFromHome"),
                        monthly_income=row.get("MonthlyIncome"),
                        overtime=row.get("OverTime"),
                        prediction=pred,
                        status=status_label
                    )
                )

            AttritionPrediction.objects.bulk_create(records)
            return Response({"type": "csv", "predictions": preds.tolist()})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # 2. Manual single prediction
    data = request.data
    if data and not csv_file:
        try:
            features = [
                data.get("Age"),
                data.get("DailyRate"),
                data.get("DistanceFromHome"),
                data.get("MonthlyIncome"),
                data.get("OverTime")
            ]
            df = pd.DataFrame([features], columns=["Age","DailyRate","DistanceFromHome","MonthlyIncome","OverTime"])
            pred = int(rf_model.predict(df)[0])
            status_label = "Will Leave" if pred == 1 else "Will Stay"

            # Save into DB
            AttritionPrediction.objects.create(
                age=data.get("Age"),
                daily_rate=data.get("DailyRate"),
                distance_from_home=data.get("DistanceFromHome"),
                monthly_income=data.get("MonthlyIncome"),
                overtime=data.get("OverTime"),
                prediction=pred,
                status=status_label
            )

            return Response({"type": "single", "prediction": pred, "status": status_label})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # 3. No input
    return Response({"error": "No input provided"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_predictions(request):
    """
    Get all saved predictions
    """
    predictions = AttritionPrediction.objects.all().order_by("-created_at")
    serializer = AttritionPredictionSerializer(predictions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_prediction_detail(request, pk):
    """
    Get one prediction by ID
    """
    try:
        prediction = AttritionPrediction.objects.get(pk=pk)
    except AttritionPrediction.DoesNotExist:
        return Response({"error": "Prediction not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AttritionPredictionSerializer(prediction)
    return Response(serializer.data)
