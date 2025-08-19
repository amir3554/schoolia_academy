from django.urls import path
from . import views


urlpatterns = [
    path('stripe/config/publishable-key/', views.get_publishable_key, name='GetPublishableKey'),
    path('stripe/<int:course_id>', views.stripe_transaction, name="StripeTransaction"),
    path('stripe/webhook/', views.stripe_webhook, name='StripeWebhook'),
    path('check-out/<int:course_id>/', views.check_out, name='CheckOut'),
    path('check-out-complete/', views.check_out_complete, name='CheckOutComplete'),
    
]
