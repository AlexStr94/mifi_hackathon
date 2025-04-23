from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .v1.accointing.views import BankViewSet, CategoryViewSet, TransactionViewSet

router_v1 = SimpleRouter()
router_v1.register('v1/transactions', TransactionViewSet)
router_v1.register('v1/banks', BankViewSet)
router_v1.register('v1/categories', CategoryViewSet)

urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += router_v1.urls
