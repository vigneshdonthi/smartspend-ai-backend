from django.urls import path
from .views import PDFReportAPIView, ExcelReportAPIView

urlpatterns = [
    path("pdf/", PDFReportAPIView.as_view(), name="pdf-report"),
    path("excel/", ExcelReportAPIView.as_view(), name="excel-report")
]