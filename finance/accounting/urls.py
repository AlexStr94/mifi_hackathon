from django.urls import path

from . import views


app_name = 'accounting'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('logout/', views.logout_view, name='logout'),
    path("accounts/profile/", views.ProfileView.as_view(), name="profile"),
    path("transactions/", views.TransactionListView.as_view(), name="transactions"),
    path("transactions/create", views.TransactionCreateView.as_view(), name="create-transaction"),
    path("transactions/update/<int:id>", views.TransactionUpdateView.as_view(), name="update-transaction"),
    path("transactions/delete/<int:id>", views.TransactionDeleteView.as_view(), name="delete-transaction"),
    path('register/', views.register, name='register'),
]
