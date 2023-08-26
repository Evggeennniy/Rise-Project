# from django.contrib import admin
from django.urls import path
from accounts import views as account_views


"""
Посилання програми.
"""
urlpatterns = [
    path('sign_up', account_views.SingUpView.as_view(), name='sign_up'),
    path('profile', account_views.UserUpdateView.as_view(), name='user_profile'),
    path('choose_payment', account_views.ChoosePaymentView.as_view(), name='choose_payment'),
    path('paypal', account_views.PayPalView.as_view(), name='paypal'),
    path('paypal_callback', account_views.PayPalCallbackView.as_view(), name='paypal_callback'),
    path('liqpay', account_views.LiqPayView.as_view(), name='liqpay'),
    path('liqpay_callback', account_views.LiqPayCallbackView.as_view(), name='liqpay_callback'),
    path('sign_up/complete', account_views.UserCreateSuccesfull.as_view(), name='user_created'),
]
