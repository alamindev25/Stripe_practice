from payments.models import Payment

# Check all payments
payments = Payment.objects.all()
print(f"Total payments: {payments.count()}")

for payment in payments:
    print(f"ID: {payment.id}, Amount: ${payment.amount}, Status: {payment.status}, Created: {payment.created_at}")
    
# Check by status
pending = Payment.objects.filter(status="pending").count()
succeeded = Payment.objects.filter(status="succeeded").count()
failed = Payment.objects.filter(status="failed").count()

print(f"\nPending: {pending}, Succeeded: {succeeded}, Failed: {failed}")