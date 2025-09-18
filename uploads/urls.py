from django.urls import path
from . import views
urlpatterns = [
    path('new/', views.upload_file, name='upload_file'),
    path('preview/<int:pk>/', views.preview, name='preview'),
]
