from django.urls import path
from . import views


app_name = 'reports'

urlpatterns = [
    path('', views.report, name='report'),
    path('pdf/', views.pdf, name='pdf'),
    path('pdf2/', views.render_pdf_view, name='test_view'),
]
