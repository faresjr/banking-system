from django import forms
from .models import Transaction, Transfer, BankAccount
from django.contrib.auth.models import User

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'description']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Transaction amount must be positive.") 
        return amount

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['sender_account', 'receiver_account', 'amount', 'description']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Transfer amount must be positive.")
        return amount

class UserSearchForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='Search User')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("User does not exist.")
        return username
    
    
class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label='Deposit Amount')
    description = forms.CharField(max_length=255, required=False, label='Description', widget=forms.Textarea(attrs={'rows': 4, 'cols': 55, 'style': 'resize: none'}))
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Deposit amount must be positive.")
        return amount
    
class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label='Withdrawal Amount')
    description = forms.CharField(max_length=255, required=False, label='Description', widget=forms.Textarea(attrs={'rows': 4, 'cols': 55, 'style': 'resize: none'}))

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Withdrawal amount must be positive.")
        return amount


class TransferForm(forms.Form):
    receiver_account = forms.ModelChoiceField(queryset=BankAccount.objects.all(), required=True, label='Receiver Account')
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label='Transfer Amount')
    description = forms.CharField(max_length=255, required=False, label='Description', widget=forms.Textarea(attrs={'rows': 4, 'cols': 55, 'style': 'resize: none'}))

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Transfer amount must be positive.")
        return amount