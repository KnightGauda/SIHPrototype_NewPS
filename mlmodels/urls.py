from django.urls import path
from . import views
urlpatterns = [
    path('', views.predict_menu, name='predict_menu'),
    path('run/', views.run_prediction, name='run_prediction'),
]
