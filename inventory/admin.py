from django.contrib import admin

# Register your models here.

from .models import Account, BalanceReport, GoldPrice


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('name',)}),
    )


@admin.register(GoldPrice)
class GoldPriceAdmin(admin.ModelAdmin):
    list_display = ('date', 'price', 'created_at', 'updated_at')
    list_filter = ('date', 'price', 'created_at', 'updated_at')
    search_fields = ('date', 'price', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('date', 'price', 'created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('date', 'price',)}),
    )


@admin.register(BalanceReport)
class BalanceReportAdmin(admin.ModelAdmin):
    list_display = ('account', 'gold_price', 'receivable', 'payable',
                    'rati', 'gold', 'cash_in', 'cash_out', 'created_at', 'updated_at')
    list_filter = ('account', 'gold_price', 'receivable', 'payable',
                   'rati', 'gold', 'cash_in', 'cash_out', 'created_at', 'updated_at')
    search_fields = ('account', 'gold_price', 'receivable', 'payable',
                     'rati', 'gold', 'cash_in', 'cash_out', 'created_at', 'updated_at')
    
    ordering = ('account', 'gold_price', 'receivable', 'payable',
                'rati', 'gold', 'cash_in', 'cash_out', 'created_at', 'updated_at')
    
    
