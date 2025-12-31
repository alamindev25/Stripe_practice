from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import stripe
import json
from .models import Payment
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY



# Frontend Payment Page
def payment_page(request):
    return render(request, "payments/pay.html", {"stripe_publishable_key": settings.STRIPE_PUBLISHABLE_KEY})

# Webhook Test Dashboard
def webhook_test_page(request):
    return render(request, "payments/webhook_test.html")

# Create PaymentIntent API
class CreatePaymentIntent(APIView):
    def post(self, request):
        try:
            amount = request.data.get("amount")
            email = request.data.get("email", "test@example.com")
            
            if not amount:
                return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            if float(amount) < 0.50:
                return Response({"error": "Minimum amount is $0.50"}, status=status.HTTP_400_BAD_REQUEST)

            intent = stripe.PaymentIntent.create(
                amount=int(float(amount) * 100),  # Convert to cents
                currency="usd",
                metadata={'email': email}
            )

            Payment.objects.create(
                amount=amount,
                stripe_payment_intent=intent.id,
                status="pending"
            )

            return Response({
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id
            })
            
        except ValueError as e:
            return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response({"error": f"Stripe error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Webhook to handle payment success
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    # Debug logging
    print("=== WEBHOOK RECEIVED ===")
    print(f"Method: {request.method}")
    print(f"Content-Type: {request.content_type}")
    print(f"Signature: {sig_header}")
    print(f"Payload length: {len(payload)}")
    print(f"Endpoint Secret: {endpoint_secret}")
    
    # For testing without real webhook secret
    if not endpoint_secret or endpoint_secret == "whsec_your_webhook_secret_here":
        print("⚠️  WARNING: Using test mode without webhook verification")
        try:
            # Parse payload without verification for testing
            event = json.loads(payload.decode('utf-8'))
            print(f"Event type: {event.get('type')}")
        except Exception as e:
            print(f"Error parsing payload: {e}")
            return JsonResponse({'error': 'Invalid payload'}, status=400)
    else:
        # Production webhook verification
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            print("❌ Invalid payload")
            return JsonResponse({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError:
            print("❌ Invalid signature")
            return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        stripe_id = payment_intent['id']
        print(f"✅ Processing successful payment: {stripe_id}")
        try:
            payment = Payment.objects.get(stripe_payment_intent=stripe_id)
            payment.status = "succeeded"
            payment.save()
            print(f"✅ Payment {stripe_id} marked as succeeded")
        except Payment.DoesNotExist:
            print(f"⚠️  Payment {stripe_id} not found in database")
            
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        stripe_id = payment_intent['id']
        print(f"❌ Processing failed payment: {stripe_id}")
        try:
            payment = Payment.objects.get(stripe_payment_intent=stripe_id)
            payment.status = "failed"
            payment.save()
            print(f"❌ Payment {stripe_id} marked as failed")
        except Payment.DoesNotExist:
            print(f"⚠️  Payment {stripe_id} not found in database")
    else:
        print(f"ℹ️  Unhandled event type: {event['type']}")

    print("=== WEBHOOK COMPLETED ===")
    return JsonResponse({'status': 'success', 'event_type': event.get('type')})

# API to get payment status
class PaymentStatusAPI(APIView):
    def get(self, request):
        payments = Payment.objects.all()
        payment_data = []
        for payment in payments:
            payment_data.append({
                'id': payment.id,
                'amount': float(payment.amount),
                'status': payment.status,
                'stripe_payment_intent': payment.stripe_payment_intent,
                'created_at': payment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'user': str(payment.user) if payment.user else 'Anonymous'
            })
        return Response(payment_data)

# Simple Payment Status Page
def payment_status_page(request):
    payments = Payment.objects.all()
    
    # Calculate status counts
    total_count = payments.count()
    pending_count = payments.filter(status='pending').count()
    succeeded_count = payments.filter(status='succeeded').count()
    failed_count = payments.filter(status='failed').count()
    
    context = {
        'payments': payments,
        'total_count': total_count,
        'pending_count': pending_count,
        'succeeded_count': succeeded_count,
        'failed_count': failed_count
    }
    
    return render(request, "payments/simple_status.html", context)
