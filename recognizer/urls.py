from django.urls import path
from .views import record_audio, analyze_audio

urlpatterns = [
    path('', record_audio, name='record_audio'),
    path('analyze/', analyze_audio, name='analyze_audio'),
]