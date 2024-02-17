from django.views import generic
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from bank.exceptions import InvalidAccountException, InvalidTransferException

from bank.models import Account, Transaction, Transfer

from .forms import *

class LoginRedirectView(generic.RedirectView):
    permanent = True
    pattern_name = 'login'

class LogoutView(generic.RedirectView):
    permanent = True
    pattern_name = 'login'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login/')

# CREATE ----------------------------------------------------------------------

class RegisterView(generic.FormView):
    template_name = 'bank/register.html'
    form_class = RegisterForm
    success_url = '/login/'

    def form_valid(self, form):
        form.register_user()
        return super().form_valid(form)

class AccountCreateView(generic.FormView):
    template_name = 'bank/account.html'
    form_class = AccountForm
    success_url = '/accounts/'

    def form_valid(self, form):
        form.create_account(self.request.user)
        return super().form_valid(form)

# READ ------------------------------------------------------------------------

class AccountsView(generic.ListView):
    template_name = 'bank/accounts.html'
    context_object_name = 'account_list'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

class TransactionsView(generic.ListView):
    template_name = 'bank/transactions.html'
    context_object_name = 'transaction_list'

    def get_queryset(self):
        account = Account.objects.get(pk=self.kwargs.get('pk'))
        return Transaction.objects.filter(account=account)


# UPDATE ----------------------------------------------------------------------

class EditProfileView(generic.UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    widgets = {
        'password': forms.PasswordInput()
    }
    success_url = '/'

# DEPOSIT/WITHDRAW/TRANSFER ---------------------------------------------------

class DepositWithdrawView(generic.FormView):
    template_name = 'bank/deposit-withdraw.html'
    form_class = DepositWithdrawForm
    success_url = '/accounts/'

    def form_valid(self, form):
        account = Account.objects.get(pk=self.kwargs.get('pk'))
        if account.status != Account.Status.ACTIVE:
            raise InvalidAccountException
        form.create_transaction(account)
        return super().form_valid(form)

class TransferView(generic.CreateView):
    template_name = 'bank/transfer.html'
    form_class = TransferForm
    success_url = '/accounts/'

    def get_form_kwargs(self):
        kwargs = super(TransferView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        source = Account.objects.get(pk=form.data.get('source'))
        print("Source: " + str(source))
        destination = Account.objects.get(pk=form.data.get('destination'))
        print("Destination: " + str(source))

        if source.status != Account.Status.ACTIVE:
            # raise InvalidAccountException
            return HttpResponseRedirect('/accounts/invalid-transaction/')
        if destination.status != Account.Status.ACTIVE:
            # raise InvalidTransferException
            return HttpResponseRedirect('/accounts/invalid-transfer/')
        if source == destination:
            # raise InvalidTransferException
            return HttpResponseRedirect('/accounts/invalid-transfer')
        try:
            user = self.request.user
            form.transfer()
            return super().form_valid(form)
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/accounts/invalid-account')

