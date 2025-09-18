from django.shortcuts import render, redirect
import numpy as np

def predict_menu(request):
    return render(request, 'predict.html')

def run_prediction(request):
    # This is a stubbed predictor for prototype. Replace with model loading.
    # Expects CSV upload or operates on last uploaded file in real app.
    results = {
        'numerical': {'yield_kg': 1200, 'biodiversity_index': 2.8},
        'categorized': {'yield': 'High', 'biodiversity': 'Moderate', 'water_quality': 'Safe'}
    }
    return render(request, 'results.html', {'results': results})
