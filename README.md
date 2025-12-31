# 💳 Stripe Payment Integration with Django

A complete Django application for handling Stripe payments with webhook integration and real-time status monitoring.

## 🚀 Features

- ✅ Stripe Payment Intent Integration
- ✅ Real-time Webhook Processing  
- ✅ Automatic Payment Status Updates
- ✅ Payment Status Dashboard
- ✅ Admin Panel Integration
- ✅ Test Card Support
- ✅ Error Handling & Validation

## 📋 Prerequisites

- Python 3.8+
- Django 6.0
- Stripe Account (Test Mode)

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/alamindev25/Stripe_practice.git
cd Stripe_practice
```

### 2. Create Virtual Environment
```bash
python -m venv env
env\Scripts\activate  # Windows
# source env/bin/activate  # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your Stripe keys:
# Get keys from: https://dashboard.stripe.com/test/apikeys
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

## 🎯 Usage

### Payment Testing
1. Visit: http://127.0.0.1:8000/payments/
2. Use test card: `4242 4242 4242 4242`
3. Enter any future expiry date and CVC
4. Submit payment

### Status Monitoring
- **Dashboard**: http://127.0.0.1:8000/payments/status/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Webhook Test**: http://127.0.0.1:8000/payments/test-webhook/

## 💳 Test Cards

| Card Number | Description |
|------------|-------------|
| `4242 4242 4242 4242` | Visa - Success |
| `4000 0000 0000 0002` | Generic Decline |
| `4000 0000 0000 9995` | Insufficient Funds |
| `4000 0027 6000 3184` | 3D Secure Required |

## 🔔 Webhook Integration

The application automatically handles Stripe webhooks for:
- `payment_intent.succeeded` → Updates status to "succeeded"
- `payment_intent.payment_failed` → Updates status to "failed"

### Production Webhook Setup
1. Go to Stripe Dashboard → Webhooks
2. Add endpoint: `https://yourdomain.com/payments/webhook/`
3. Select events: `payment_intent.succeeded`, `payment_intent.payment_failed`
4. Copy webhook secret to `.env` file

## 📁 Project Structure

```
stripe_project/
├── payments/                 # Main payment app
│   ├── templates/           # HTML templates
│   ├── models.py           # Payment model
│   ├── views.py            # Views and API endpoints
│   ├── urls.py             # URL routing
│   └── admin.py            # Admin configuration
├── stripe_project/          # Django project settings
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # Project documentation
```

## 🔧 API Endpoints

- `GET /payments/` - Payment form page
- `POST /payments/create-payment-intent/` - Create payment intent
- `POST /payments/webhook/` - Stripe webhook handler
- `GET /payments/status/` - Payment status dashboard
- `GET /payments/api/payments/` - Payment data API

## 🛡️ Security Features

- Environment variables for sensitive data
- Webhook signature verification
- CSRF protection
- Input validation and sanitization
- Error handling and logging

## 📱 Screenshots

### Payment Form
- Clean, responsive payment interface
- Real-time validation
- Test card information display

### Status Dashboard  
- Live payment monitoring
- Auto-refresh functionality
- Status statistics and charts

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the troubleshooting section
2. Review Stripe documentation
3. Open an issue on GitHub

## 🔗 Useful Links

- [Stripe Documentation](https://stripe.com/docs)
- [Django Documentation](https://docs.djangoproject.com/)
- [Stripe Test Cards](https://stripe.com/docs/testing#cards)

---

**Made with ❤️ for learning Stripe integration**