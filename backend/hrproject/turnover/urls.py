from django.urls import path

from . import views




urlpatterns = [
    path("predictAttrition/", views.predictAttrition, name="predict_attrition"),   # POST to create a prediction

    path("predictions_attritions/", views.get_predictions, name="get_predictions"),  # GET all predictions

    path("predictions/<int:pk>/", views.get_prediction_detail, name="get_prediction_detail"),  # GET one prediction
]
