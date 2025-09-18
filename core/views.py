# core/views.py
from django.shortcuts import render
from django.http import JsonResponse
from uploads.models import UploadedFile
import pandas as pd
import numpy as np

def landing(request):
    return render(request, 'landing.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def dashboard_data(request):
    """
    Returns JSON payload for charts and maps from the most recent uploaded file.
    """
    obj = UploadedFile.objects.order_by('-uploaded_at').first()
    if not obj:
        return JsonResponse({'error': 'No uploaded files found.'}, status=404)

    # Read uploaded file
    try:
        fp = obj.file.path
        if fp.lower().endswith('.csv'):
            df = pd.read_csv(fp)
        else:
            df = pd.read_excel(fp)
    except Exception as e:
        return JsonResponse({'error': f'Error reading uploaded file: {e}'}, status=500)

    # Detect species columns
    species_cols = [c for c in df.columns if 'Species' in c and 'Count' in c]
    if not species_cols:
        species_cols = [c for c in df.columns if c.lower().startswith(('species', 'fish'))]

    # Chart 1: species sums
    species_sums = {}
    for c in species_cols:
        try:
            val = pd.to_numeric(df[c], errors='coerce').sum(skipna=True)
            species_sums[c] = int(val)
        except Exception:
            species_sums[c] = 0

    # Chart 2: temp vs abundance
    df['_row_abundance'] = df[species_cols].apply(pd.to_numeric, errors='coerce').sum(axis=1) if species_cols else 0
    temp_vs_abundance = []
    if 'Temperature_C' in df.columns:
        for t, a in zip(df['Temperature_C'], df['_row_abundance']):
            try:
                temp_vs_abundance.append({
                    'temperature': float(t),
                    'abundance': float(a)
                })
            except Exception:
                continue

    # Chart 3: biodiversity composition
    total = sum(species_sums.values())
    biodiversity = []
    if total > 0:
        for k, v in species_sums.items():
            biodiversity.append({
                'species': k,
                'count': int(v),
                'pct': float(v) / float(total)
            })

    # Map data
    map_points = []
    if {'Latitude', 'Longitude'}.issubset(df.columns):
        for _, row in df.iterrows():
            try:
                map_points.append({
                    'site': str(row.get('Site', '')),
                    'lat': float(row['Latitude']),
                    'lon': float(row['Longitude']),
                    'abundance': float(row.get('_row_abundance', 0))
                })
            except Exception:
                continue

    # Summary
    summary = {
        'predicted_yield_kg': int(df['Total_Catch_kg'].sum()) if 'Total_Catch_kg' in df.columns else None,
        'biodiversity_index': float(round(np.log1p(total), 2)) if total > 0 else 0.0,
        'water_quality_counts': {str(k): int(v) for k, v in df['Water_Quality'].value_counts().items()} if 'Water_Quality' in df.columns else {}
    }

    payload = {
        'file_name': obj.name,
        'species_sums': species_sums,
        'temp_vs_abundance': temp_vs_abundance,
        'biodiversity': biodiversity,
        'map_points': map_points,
        'summary': summary,
    }
    return JsonResponse(payload)
