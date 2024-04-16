from django.urls import path
from . import eth_operations
from . import views

urlpatterns = [
    path('', views.base, name='finance_base'),
    path('dashboard/', views.dashboard, name='finance_dashboard'),
    path('api/', views.api_receive_data, name='finance_api_receive_data'),
    path('display_data/', views.display_data, name='finance_display_data'),
    path('contract_interaction/', eth_operations.contract_interaction, name='finance_contract_interaction'),
    path('products/', views.products, name='finance_products'),
    path('sell_product/<int:product_id>/', views.sell_product, name='sell_product'),
    path('ethereum_demo/', views.ethereum_demo, name='ethereum_demo'),
    path('contract_interaction/<str:account>/', eth_operations.contract_interaction,name='finance_contract_interaction'),
    path('deposit_tokens/<str:account>/', views.deposit_tokens_view, name='finance_deposit_tokens'),
    path('get_balance/<str:account>/', eth_operations.get_balance, name='finance_get_balance'),
    path('get_user_balance/', views.get_user_balance, name='get_user_balance'),
    path('donate/', views.donate_view, name='donate'),
]
