from django.contrib import admin
from .models import Subscription, Transaction, Prepare, Payment, Complete


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'status')
    list_display_links = ('id', 'user')
    search_fields = ('status',)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Transaction)
class CreateTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'payme_id', 'amount', 'state', 'time')
    list_display_links = ('id', 'payme_id')
    search_fields = ('state', 'payme_id')

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id',)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Complete)
class CompleteAdmin(admin.ModelAdmin):
    list_display = ('id',)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Prepare)
class PrepareAdmin(admin.ModelAdmin):
    list_display = ('id',)

    def has_change_permission(self, request, obj=None):
        return False
