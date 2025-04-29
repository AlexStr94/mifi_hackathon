from django.urls import path
from . import views

app_name = 'dashboard'  # Добавляем namespace

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('transaction-dynamics/', views.transaction_dynamics, name='transaction-dynamics'),
    path('transaction-type-stats/', views.transaction_type_stats, name='transaction-type-stats'),
    path('income-vs-expense/', views.income_vs_expense, name='income-vs-expense'),
    path('transaction-status-stats/', views.transaction_status_stats, name='transaction-status-stats'),
    path('bank-stats/', views.bank_stats, name='bank-stats'),
    path('category-stats/', views.category_stats, name='category-stats'),
]