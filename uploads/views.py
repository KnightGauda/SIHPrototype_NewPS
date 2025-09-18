import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm
from .models import UploadedFile

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            obj = UploadedFile.objects.create(name=f.name, file=f)
            return redirect('preview', pk=obj.pk)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def preview(request, pk):
    obj = get_object_or_404(UploadedFile, pk=pk)
    # read with pandas (works for csv/xlsx if engine installed)
    file_path = obj.file.path
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        preview_html = df.head(5).to_html(classes='table table-striped', index=False)
    except Exception as e:
        preview_html = f"<pre>Error reading file: {e}</pre>"
    return render(request, 'preview.html', {'object': obj, 'preview_html': preview_html})
