from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import decimal

# Account ---------------------------------------------------------------------

class Account(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        INACTIVE = 'INACTIVE', _('Inactive')
        DEACTIVATED = 'DEACTIVATED', _('Deactivated')
    
    class Type(models.TextChoices):
        CHECKING = 'CHECKING', _('Checking')
        SAVINGS = 'SAVINGS', _('Savings')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.CHECKING)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INACTIVE)
    balance = models.DecimalField(max_digits=14, decimal_places=2)
    
    def __str__(self):
        return str(self.id)

# Transaction -----------------------------------------------------------------

class Transaction(models.Model):
    class Type(models.TextChoices):
        CREDIT = 'CREDIT', _('Deposit')
        DEBIT = 'DEBIT', _('Withdraw')
        TRANSFER = 'TRANSFER', _('Transfer')

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=Type.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(decimal.Decimal('0.01'))])
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)

class Transfer(models.Model):
    source = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfer_sources')
    destination = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfer_destinations')
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(decimal.Decimal('0.01'))])
    description = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)

