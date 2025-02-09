from django.urls import path
from . import views

urlpatterns = [
    path('', views.wallet, name='wallet'),
    path('wallet/driver/', views.wallet_driver, name='wallet_driver'),
    path('wallet/student/', views.wallet_student, name='wallet_student'), 
    path('wallet/balance/<str:user_type>/<int:user_id>/', views.wallet_balance, name='wallet_balance'),
    path('wallet/deposit/<str:user_type>/<int:user_id>/', views.deposit, name='wallet_deposit'),
    path('wallet/withdraw/<str:user_type>/<int:user_id>/', views.withdraw, name='wallet_withdraw'),
    path('wallet/refund/<str:user_type>/<int:user_id>/', views.refund, name='wallet_refund'),
    path('wallet/history/<str:user_type>/<int:user_id>/', views.wallet_transaction_history, name='wallet_transaction_history'),
]
