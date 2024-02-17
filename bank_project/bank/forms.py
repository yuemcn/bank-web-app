import decimal
from django import forms
from django.contrib.auth.models import User

from .models import Account, Transaction, Transfer

# Register User ---------------------------------------------------------------

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def register_user(self):
        user = User.objects.create_user(
            self.data['username'],
            email=self.data['email'],
            password=self.data['password'],
        )
        user.first_name = self.data['first_name']
        user.last_name = self.data['last_name']
        user.save()

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['type']
    
    def create_account(self, user):
        account = Account(
            user = user,
            balance = 0,
            status = Account.Status.INACTIVE,
            type = self.data['type']
        )
        account.save()

# Transactions ----------------------------------------------------------------

class DepositWithdrawForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount']
    
    def create_transaction(self, account):
        transaction = Transaction(
            account = account,
            amount = self.data['amount'],
            type = self.data['type']
        )
        if self.data['type'] == Transaction.Type.CREDIT:
            account.balance += decimal.Decimal(self.data['amount'])
            transaction.description = "Credit to account #" + str(account.id)
        else:
            account.balance -= decimal.Decimal(self.data['amount'])
            transaction.description = "Debit from account #" + str(account.id)
        transaction.save()
        account.save()

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['source', 'destination', 'amount']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields['source'].queryset = Account.objects.filter(user=user)
        self.fields['destination'].queryset = Account.objects.filter(user=user)
    
    def transfer(self):
        src = Account.objects.get(pk=self.data['source'])
        dest = Account.objects.get(pk=self.data['destination'])

        debit = Transaction(
            account = src,
            type = Transaction.Type.DEBIT,
            amount = decimal.Decimal(self.data['amount']),
            description = "Transfer to Account #" + str(dest.id)
        )
        src.balance -= decimal.Decimal(self.data['amount'])
        src.save()
        debit.save()
        credit = Transaction(
            account = dest,
            type = Transaction.Type.CREDIT,
            amount = decimal.Decimal(self.data['amount']),
            description = "Transfer from Account #" + str(src.id)
        )
        dest.balance += decimal.Decimal(self.data['amount'])
        dest.save()
        credit.save()

