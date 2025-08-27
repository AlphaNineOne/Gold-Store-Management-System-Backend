from .models import BalanceReport
from django_filters import rest_framework as filters


class JobFilters(filters.FilterSet):
    min_price = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    max_price = filters.DateFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = BalanceReport
        fields = ['account__name', 'created_at']
