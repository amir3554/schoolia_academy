from django.urls import path
from . import views

from paypal.standard.ipn.views import ipn

urlpatterns = [

    # Clinic
    #path('clinic-app/stripe/config/publishable-key/', views.get_publishable_key, name='ClinicGetPublishableKey'),
    #path('clinic-app/stripe/<int:appointment_id>', views.stripe_transaction_clinic, name="ClinicStripeTransaction"),
    #path('clinic-app/stripe/webhook/', views.stripe_webhook_clinic, name='ClinicStripeWebhook'),
    path('clinic-app/check-out/<int:appointment_id>/', views.check_out_clinic, name='ClinicCheckOut'),
    path('clinic-app/check-out-complete/', views.check_out_complete_clinic, name='ClinicCheckOutComplete'),
    #path('clinic-app/paypal/<int:appointment_id>/', views.paypal_transaction_clinic, name='ClinicCheckoutPaypal'),
    #path('clinic-app/paypal/webhook/', ipn, name='ClinicCheckoutPaypalWebhook'),

    # Store
    path('store-app/check-out/', views.check_out_store, name='StoreCheckout'),
    path('store-app/check-out-complete/', views.check_out_complete_store, name='StoreCheckoutComplete'),
    #path('store-app/stripe/', views.stripe_transaction_store, name='StoreStripeTransaction'),
    #path('store-app/stripe-config/', views.stripe_config, name='StoreStripeConfig'),
    #path('store-app/stripe/webhook/',views.stripe_webhook_store, name='StoreStripeWebhook'),
    #path('store-app/paypal/', views.paypal_transaction_store, name='StorePaypal'),
    #path('store-app/paypal/webhook/', ipn, name='StorePaypalWebhook'),

]
