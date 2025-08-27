from .views import *
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()

router.register('gold-price', GoldPriceViewSet)
router.register('account', AccountViewSet)
router.register('balance-report', BalanceReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
