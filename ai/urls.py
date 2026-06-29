from django.urls import path
from .views import AnalyzeAPIView

urlpatterns = [
    path('analyze/', AnalyzeAPIView.as_view(), name='analyze')
]