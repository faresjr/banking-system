from django.contrib import admin
from .models import BankAccount, Transaction, Transfer

# Register your models here.
admin.site.register(BankAccount)
admin.site.register(Transaction)
admin.site.register(Transfer)
