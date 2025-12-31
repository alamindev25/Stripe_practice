from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'stripe_payment_intent', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['stripe_payment_intent', 'user__username', 'user__email']
    readonly_fields = ['stripe_payment_intent', 'created_at']
    
    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion of payment records
