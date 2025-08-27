from rest_framework import serializers
from .models import Account, BalanceReport, GoldPrice
from django.db.models import Q
from django.db.models import Sum
from decimal import Decimal


class GoldPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldPrice
        fields = "__all__"


class UpdateGoldPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoldPrice
        fields = ["price", "id"]


class BalanceReportSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    account_name = serializers.CharField(source='account.name', read_only=True)
    total_receivable_gold = serializers.SerializerMethodField()
    total_payable_gold = serializers.SerializerMethodField()

    def get_total_receivable_gold(self, obj):
        total_receivable_gold = None
        company_id = self.context['request'].GET.get('account', None)
        if company_id:
            total_receivable_gold = BalanceReport.objects.filter(account=company_id).filter(~Q(receivable="0.000") | ~Q(cash_in="0.000")).aggregate(
                total_receivable_gold=Sum('gold'))
            if total_receivable_gold['total_receivable_gold']:
                return Decimal("{:.3f}".format(total_receivable_gold['total_receivable_gold']))

        else:
            total_receivable_gold = BalanceReport.objects.filter(~Q(receivable="0.000") | ~Q(cash_in="0.000")).aggregate(
                total_receivable_gold=Sum('gold'))
            if total_receivable_gold['total_receivable_gold']:
                return Decimal("{:.3f}".format(total_receivable_gold['total_receivable_gold']))
            return round(0.000, 3)

    def get_total_payable_gold(self, obj):
        total_payable_gold = None
        company_id = self.context['request'].GET.get('account', None)
        if company_id:
            total_payable_gold = BalanceReport.objects.filter(account=company_id).filter(~Q(payable="0.000") | ~Q(cash_out="0.000")).aggregate(
                total_payable_gold=Sum('gold'))
            if total_payable_gold['total_payable_gold']:
                return Decimal("{:.3f}".format(total_payable_gold['total_payable_gold']))
            return round(0.000, 3)

        else:
            total_payable_gold = BalanceReport.objects.filter(~Q(payable="0.000") | ~Q(cash_out="0.000")).aggregate(
                total_payable_gold=Sum('gold'))
            if total_payable_gold['total_payable_gold']:
                return Decimal("{:.3f}".format(total_payable_gold['total_payable_gold']))
            return round(0.000, 3)

    def get_balance(self, obj):
        return self.context['request'].user.balance

    class Meta:
        model = BalanceReport
        fields = "__all__"
        extra_kwargs = {
            'payable': {'required': False},
            'receivable': {'required': False},
            'cash_in': {'required': False},
            'cash_out': {'required': False},
        }


class AccountSerializer(serializers.ModelSerializer):
    balance_report = serializers.SerializerMethodField()

    def get_balance_report(self, obj):
        return BalanceReportSerializer(obj.balance_report.last(), context={'request': self.context['request']}).data

    class Meta:
        model = Account
        fields = "__all__"
