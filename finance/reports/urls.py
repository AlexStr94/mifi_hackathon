from django.urls import path
from . import views


app_name = 'reports'

urlpatterns = [
    path('', views.ReportView.as_view(), name='report'),
    path('pdf/', views.PdfView.as_view(), name='pdf'),
]
