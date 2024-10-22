from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    CheckTokenView,
    InstallmentsListByMonthYearView,
    RegisterView,
    TagViewSet,
    TransactionTypeViewSet,
    EntryViewSet,
    EntryTagViewSet,
    PeriodicTypeViewSet,
    PeriodicEntryViewSet,
    InstallmentViewSet,
)

router = DefaultRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'transaction-types', TransactionTypeViewSet)
router.register(r'entries', EntryViewSet)
router.register(r'entry-tags', EntryTagViewSet)
router.register(r'periodic-types', PeriodicTypeViewSet)
router.register(r'periodic-entries', PeriodicEntryViewSet)
router.register(r'installments', InstallmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('installments/list-month-year', InstallmentsListByMonthYearView.as_view(), name='installment-list-month-year'),
    path('token/check', CheckTokenView.as_view(), name='token-check'),
    path('register/', RegisterView.as_view(), name='register'),
]