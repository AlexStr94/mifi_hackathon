from django.urls import path

from . import views


app_name = 'accounting'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("transactions/", views.TransactionListView.as_view(), name="transactions")
]
