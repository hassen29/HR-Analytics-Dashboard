from django.urls import path

from . import views

urlpatterns = [
    path('',views.getRoutes,name="routes"),
    path('candidates/', views.getCandidates, name="candidates"),
    path('candidates/<str:pk>', views.getCandidate, name="candidat"),

    path('predict/', views.predictJob, name="job"),
    
     path('predictions/', views.getPredictions, name="predictions")

]