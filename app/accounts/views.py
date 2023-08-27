from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from accounts import forms as account_forms
from django.shortcuts import redirect, render
from liqpay.liqpay3 import LiqPay
from settings.settings import LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY, PAYPAL_CLIENT_ID, PAYPAL_SECRET_KEY
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from accounts import models as account_models
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
import paypalrestsdk
import decimal


class SingUpView(generic.CreateView):
    """
    Вид для реєстрації.
    """
    queryset = get_user_model()
    form_class = account_forms.SignUpForm
    success_url = reverse_lazy('login')
    template_name = "singup.html"


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Вигляд особистого профілю.
    """
    queryset = get_user_model().objects
    success_url = reverse_lazy('index')
    template_name = 'my_profile.html'

    fields = (
        'username',
        'email',
    )

    def get_object(self, queryset=None):
        return self.request.user


class UserCreateSuccesfull(generic.TemplateView):
    """
    Вигляд успішного створення облікового запису.
    """
    template_name = 'user_successfully_created.html'


class ChoosePaymentView(LoginRequiredMixin, generic.CreateView):
    """
    Вигляд до вибору платежу.
    """
    queryset = account_models.Payment
    form_class = account_forms.ChoosePaymentForm
    success_url = reverse_lazy('paypal')
    template_name = 'choosepayment.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['client_id'] = self.request.user.id
        return kwargs


class PayPalView(LoginRequiredMixin, generic.TemplateView):
    """
    Вигляд до плати на paypal вiджети.
    """
    api = paypalrestsdk.configure({
    "mode": "live",
    "client_id": PAYPAL_CLIENT_ID,
    "client_secret": PAYPAL_SECRET_KEY
    })
    template_name = 'paypal_payment.html'

    def get(self, request, *args, **kwargs):
        last_payment = account_models.Payment.objects.filter(
            client_id=self.request.user.id
        ).last()

        paypal_payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_url(reverse('paypal_callback')),
            "cancel_url": request.build_absolute_url(reverse('index'))
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Пополнение баланса",
                    "sku": "Item SKU",
                    "price": str(last_payment.value),
                    "currency": last_payment.fonds,
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(last_payment.value),
                "currency": last_payment.fonds,
            },
            "description": "Плата на Rise.ua"
        }]
        }, api=self.api)

        if paypal_payment.create():         
            return redirect(paypal_payment.links[1].href)
        else:
            return render(request, 'payment_app/error.html')


class PayPalCallbackView(LoginRequiredMixin, generic.RedirectView):
    """
    Вигляд для калл беку paypal.
    """
    pattern_name = 'index'

    def get(self, request, *args, **kwargs):
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')

        paypal_payment = paypalrestsdk.Payment.find(payment_id)
        payments = account_models.Payment.objects.filter(
            client_id=self.request.user.id
        ).select_related('client')
        full_success_payment_value = sum(payment.value for payment in payments if payment.status == 'completed')
        last_payment = payments.last()
        client = last_payment.client

        if paypal_payment.execute({"payer_id": payer_id}):
            last_payment.status = 'completed'
            payment_price = last_payment.value
            payment_fonds = last_payment.fonds

            client.balance += decimal.Decimal(payment_price)
            if (payment_fonds == 'USD' and payment_price >= 200) or \
                (payment_fonds == 'EUR' and payment_price >= 180) or \
                    (full_success_payment_value >= 500):
                client.profile_status = 'reseller'
            client.save()
        else:
            last_payment.status = 'failed'

        last_payment.save()

        return super().get(request, *args, **kwargs)


class LiqPayView(LoginRequiredMixin, generic.TemplateView):
    """
    Вигляд до плати на liqpay вiджетi.
    """
    template_name = 'liqpay_payment.html'

    def get(self, request, *args, **kwargs):
        last_payment = account_models.Payment.objects.filter(
            client_id=self.request.user.id
        ).last()

        liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': float(last_payment.value),
            'currency': last_payment.fonds,
            'description': 'Плата на Rise.ua',
            'order_id': last_payment.id,
            'version': '3',
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, self.template_name, {'signature': signature, 'data': data})


@method_decorator(csrf_exempt, name='dispatch')
class LiqPayCallbackView(generic.View):
    """
    Вигляд для калл беку liqpay.
    """
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(LIQPAY_PRIVATE_KEY + data + LIQPAY_PRIVATE_KEY)

        if sign == signature:
            response = liqpay.decode_data_from_str(data)

            order_id = response.get('order_id')
            order_status = response.get('status')
            order_price = response.get('amount')
            order = account_models.Payment.objects.get(id=order_id)

            if order_status == 'success':
                order.status = 'completed'

                client = order.client
                client.balance += decimal.Decimal(order_price)
                if (order.fonds == 'USD' and order.value >= 200) or \
                    (order.fonds == 'EUR' and order.value >= 180):
                    client.status = 'reseller'
                client.save()
            else:
                order.status = 'failed'
            order.save()

        return HttpResponse()
