# views.py
import os
import pyaudio
import wave
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import os
from .utils import analyzer, recording

# /
def analyze_audio(request):
    try:
        context = analyzer()
        return render(request, 'result.html', context)
    except Exception as e:
        return render(request, 'upload.html')

@csrf_exempt
def record_audio(request):
    if request.method == 'POST':
        try:
            recording(request)
        
            return render(request, 'upload.html', {'status': 'success'})
        except Exception as e:
            return render(request, 'upload.html', {'status': 'failure'})

    return render(request, 'upload.html')
