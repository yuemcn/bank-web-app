from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'bank'
urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('<int:pk>/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/', views.LoginRedirectView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('accounts/', views.AccountsView.as_view(), name='accounts'),
    path('accounts/create/', views.AccountCreateView.as_view(), name='create-account'),
    path('accounts/<int:pk>/transaction', views.DepositWithdrawView.as_view(), name='deposit-withdraw'),
    path('accounts/invalid-transaction/', TemplateView.as_view(template_name='bank/invalid-transaction.html'), name='invalid-transaction'),
    path('accounts/<int:pk>/transactions', views.TransactionsView.as_view(), name='transactions'),
    path('accounts/transfer/', views.TransferView.as_view(), name='transfer'),
    path('accounts/invalid-transfer/', TemplateView.as_view(template_name='bank/invalid-transfer.html'), name='invalid-transfer'),
    path('accounts/invalid-account/', TemplateView.as_view(template_name='bank/invalid-account.html'), name='invalid-account'),
    path('<int:pk>/edit/', views.EditProfileView.as_view(), name='edit-profile')
]