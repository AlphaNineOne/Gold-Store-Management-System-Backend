from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from decimal import Decimal, ROUND_DOWN
from django.db.models import Sum, Q
from rest_framework import filters
from django_filters import rest_framework as backend_filters
from .models import Account, BalanceReport, GoldPrice
from .filters import JobFilters
from rest_framework.permissions import IsAuthenticated
from .serializers import AccountSerializer, GoldPriceSerializer, BalanceReportSerializer, UpdateGoldPriceSerializer


class GoldPriceViewSet(viewsets.ModelViewSet):

    queryset = GoldPrice.objects.all()

    serializer_class = GoldPriceSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'PATCH':
            return UpdateGoldPriceSerializer
        return GoldPriceSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.balance_report.exists():
            balance = request.user.balance
            total_payable_gold = instance.balance_report.filter(
                ~Q(payable="0.000") | ~Q(cash_out="0.000")).aggregate(total_payable_gold=Sum('gold'))
            total_receivable_gold = instance.balance_report.filter(
                ~Q(receivable="0.000") | ~Q(cash_in="0.000")).aggregate(total_receivable_gold=Sum('gold'))
            if total_payable_gold['total_payable_gold']:
                balance += Decimal("{:.3f}".format(
                    total_payable_gold['total_payable_gold']))

            if total_receivable_gold['total_receivable_gold']:
                balance -= Decimal("{:.3f}".format(
                    total_receivable_gold['total_receivable_gold']))
            request.user.balance = Decimal("{:.3f}".format(balance))
            request.user.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BalanceReportViewSet(viewsets.ModelViewSet):
    queryset = BalanceReport.objects.all().order_by("-id")
    serializer_class = BalanceReportSerializer
    filterset_class = JobFilters
    search_fields = ['account__name']
    permission_classes = [IsAuthenticated]

    filter_backends = [

        backend_filters.DjangoFilterBackend,
        filters.SearchFilter,
    ]

    def create(self, request, *args, **kwargs):
        payable = request.data.get('payable', None)

        receivables = request.data.get('receivable', None)
        gold_price = request.data.get('gold_price', None)
        rati = request.data.get('rati', None)
        _type = request.data.get('type', None)
        data = request.data
        data.update({"payable": payable, "receivable": receivables})
        if _type == 'gold':
            if rati == "0.000" or rati==None:
                return Response({"error": "Rati is required for gold"}, status=400)

        gold = 0.000
        cash_in = 0.000
        cash_out = 0.000

        balance = request.user.balance
        gold_price = GoldPrice.objects.get(id=gold_price).price

        if _type == "pure_gold":
            if payable:
                gold = Decimal(payable).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                balance -= gold.quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                data["receivable"] = 0.000
            elif receivables:

                gold = Decimal(str(receivables)).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                balance += gold
                data["payable"] = 0.000

        if _type == "gold":
            if payable:
                payable= Decimal(str(payable)).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                impure_gold = Decimal((
                    Decimal(payable)/Decimal(96)*Decimal(rati))).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                gold = payable - impure_gold
                balance -= gold
                data["receivable"] = 0.000

            elif receivables:
                receivable=Decimal(str(receivables)).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                impure_gold = Decimal((Decimal(receivables) /
                                       Decimal(96)*Decimal(rati))).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                gold = receivable - impure_gold
                balance += gold
                data["payable"] = 0.000

        elif _type == "cash":
            if payable:
                gold = Decimal((Decimal(payable)/Decimal(gold_price)
                                * Decimal(11.664))).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                balance -= gold
                cash_out = Decimal(str(payable))
            elif receivables:
                gold = Decimal((Decimal(receivables) /
                                Decimal(gold_price)*Decimal(11.664))).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                balance += gold
                cash_in=Decimal(str(receivables))

            data['payable'] = 0
            data['receivable'] = 0

        data['gold'] = (gold)
        data['cash_in'] = (cash_in)
        data['cash_out'] = (cash_out)

        request.user.balance = Decimal(balance).quantize(
            Decimal('0.001'), rounding=ROUND_DOWN)
        request.user.save()
        serializer = BalanceReportSerializer(
            data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        payable = request.data.get('payable', "0.000")
        receivables = request.data.get('receivable', "0.000")
        gold_price = request.data.get('gold_price', None)
        rati = request.data.get('rati', 1.000)
        _type = request.data.get('type', None)
        data = request.data
        data.update({"payable": payable, "receivable": receivables})
        gold = 0.000
        cash_in = 0.000
        cash_out = 0.000
        balance = request.user.balance
        instance_payable = self.get_object().payable
        instance_receivable = self.get_object().receivable
        instance_cash_in = self.get_object().cash_in
        instance_cash_out = self.get_object().cash_out
        instance_gold = self.get_object().gold
        gold_price = self.get_object().gold_price.price

        if _type == "pure_gold":
            if payable != "0.000" and payable:
                gold = Decimal(payable)
                balance -= gold.quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                data.update({"receivable": "0.000"})
            elif receivables != "0.000" and receivables:
                gold = Decimal(str(receivables)).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                balance += gold
                data.update({"payable": "0.000"})

        if _type == "gold":

            if payable != "0.000" and payable:
                impure_gold = Decimal((
                    Decimal(payable)/Decimal(96)*Decimal(str(rati)))).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                gold = Decimal(str(payable)) - impure_gold
                balance -= gold
            elif receivables != "0.000" and receivables:

                impure_gold = Decimal((
                    Decimal(receivables) / Decimal(96)*Decimal(rati))).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                gold = Decimal(str(receivables)) - impure_gold
                balance += gold
        elif _type == "cash":
            if payable != "0.000" and payable:

                gold = Decimal((Decimal(payable)/Decimal(gold_price)
                                * Decimal(11.664))).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                balance -= gold

                cash_out = Decimal(str(payable))
            elif receivables != "0.000" and receivables:
                gold = (Decimal(receivables)/Decimal(gold_price)*Decimal(11.664)).quantize(
                    Decimal('0.001'), rounding=ROUND_DOWN)
                balance += Decimal(gold)
                cash_in = Decimal(str(receivables))
            data['payable'] = "0.000"
            data['receivable'] = "0.000"

        data['gold'] = Decimal(gold)
        if instance_payable != Decimal(0.000):
            balance += instance_gold
        elif instance_receivable != Decimal(0.000):
            balance -= instance_gold
        elif instance_cash_in != Decimal(0.000):
            balance -= instance_gold

        elif instance_cash_out != Decimal(0.000):
            balance += instance_gold

        request.user.balance = Decimal((balance)).quantize(
            Decimal('0.001'), rounding=ROUND_DOWN)
        request.user.save()
        data['cash_in'] = cash_in
        data['cash_out'] = cash_out
        instance = self.get_object()
        serializer = BalanceReportSerializer(
            instance, data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        account = self.request.query_params.get('account', None)
        from_date = request.GET.get('min_price')
        to_date = request.GET.get('max_price')
        print(from_date, to_date)
        queryset = BalanceReport.objects.all().order_by('-id')
        if account:
            queryset = queryset.filter(account=account)
        if from_date and to_date:
            queryset = queryset.filter(
                created_at__range=[from_date, to_date])
        serializer = BalanceReportSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        balance = request.user.balance

        if instance.payable != "0.000":
            balance += instance.gold
        elif instance.receivable != "0.000":
            balance -= instance.gold
        if instance.cash_in != "0.000":
            balance -= instance.gold
        elif instance.cash_out != "0.000":
            balance += instance.gold
        request.user.balance = Decimal("{:.3f}".format(balance))
        request.user.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
