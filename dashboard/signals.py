from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import BankAccount

# Signal to create a BankAccount when a new User is created
@receiver(post_save, sender=User)
def create_bank_account(sender, instance, created, **kwargs):
    if created:
        BankAccount.objects.create(user=instance)