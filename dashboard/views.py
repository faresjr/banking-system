from django.shortcuts import render, redirect
from .models import BankAccount, Transaction, Transfer
from .forms import TransferForm, DepositForm, WithdrawalForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
def dashboard(request):
    # Fetch user bank account details
    if request.user.is_authenticated:
        try:
            account = BankAccount.objects.get(user=request.user)
            transactions = Transaction.objects.filter(account=account).order_by('created_at')
            paginator = Paginator(transactions, 8)  # Show 10 transactions per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {'account': account, 'balance': account.balance, 'transactions': page_obj}
        except BankAccount.DoesNotExist:
            context = {'error': "Bank account not found."}
    else:
        context = {'error': "User not authenticated."}
    return render(request, 'main/dashboard.html', context)


@login_required
def transaction(request):
    # Make a transaction
    if request.method == 'POST':
        account = BankAccount.objects.get(user=request.user)
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')

        if transaction_type == 'deposit':

            account.balance += float(amount)
            account.save()

        elif transaction_type == 'withdrawal':

            if account.balance >= float(amount):
                account.balance -= float(amount)
                account.save()
            else:
                messages.error(request, "Insufficient balance.")

        else:
            messages.error(request, "Invalid transaction type.")


@login_required
def deposit(request):
    # Handle deposit logic
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            account = BankAccount.objects.get(user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit', description=description)
            messages.success(request, "Deposit successful.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid deposit amount.")
    else:
        form = DepositForm()

    context = {'form': form}

    return render(request, 'main/deposit.html', context)


@login_required
def withdrawal(request):
    # Handle withdrawal logic
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            account = BankAccount.objects.get(user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal', description=description)
                messages.success(request, "Withdrawal successful.")
                return redirect('dashboard')
            else:
                messages.error(request, "Insufficient balance.")
        else:
            messages.error(request, "Invalid withdrawal amount.")
    else:
        form = WithdrawalForm()

    context = {'form': form}

    return render(request, 'main/withdrawal.html', context)


@login_required
def transfer(request):
    if request.method == 'POST':
        # Handle transfer logic
        sender_account = BankAccount.objects.get(user=request.user)
        form = TransferForm(request.POST)
        if form.is_valid():
            receiver_account = form.cleaned_data['receiver_account']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']

            if sender_account.balance >= amount:
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()
                Transfer.objects.create(sender_account=sender_account, receiver_account=receiver_account, amount=amount, description=description)
                messages.success(request, "Transfer successful.")
                return redirect('dashboard')
            else:
                messages.error(request, "Insufficient balance.")
        else:
            messages.error(request, "Invalid transfer details.")
    else:
        form = TransferForm()

    context = {'form': form}
    return render(request, 'main/transfer.html', context)


