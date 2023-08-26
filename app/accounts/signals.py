# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from accounts.models import Payment


# @receiver(pre_save, sender=Payment)
# def update_client_status(sender, instance, **kwargs)
#     client = instance.client
#     if (instance.fonds == 'UAH' and instance.value >= 7500) or \
#         (instance.fonds == 'USD' and instance.value >= 200) or \
#         (instance.fonds == 'EUR' and instance.value >= 180):
#         if client.profile_status != 'reseller':
#             client.status = 'reseller'
#             client.save()
#     elif client.balance >= 18000:
#         client.status = 'reseller'
#         client.save()