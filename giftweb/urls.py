

# urls.py 

from django.urls import path
from .views import *

app_name = 'giftweb'

urlpatterns = [
    path('', home, name='home'),
    path('documents', documentHome, name='documents'),
    path('business', businessHome, name='business'),
    path('about/', about, name='about'),
    path('policy/', policy, name='policy'),
    path('contact/', contact, name='contact'),
    path('blogs/', blog_list, name='blog_list'),

    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('document/<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('business/<int:pk>/', BusinessView.as_view(), name='business_detail'),
    path('make_payment/<str:model_name>/<int:product_id>/', make_payment, name='make_payment'),
    path('make_crypto_payment/<str:model_name>/<int:product_id>/', make_crypto_payment, name='make_crypto_payment'),


    path('payment_success/', payment_success, name='payment_success'),
    path('crypto_payment_success/', crypto_payment_success, name='crypto_payment_success'),
    path('products/category/<str:category_name>/', products_by_category, name='products_by_category'),
    path('documents/category/<str:category_name>/', documents_by_category, name='documents_by_category'),

    
    # Add the following URL for payment history
    path('payment_history/', payment_history, name='payment_history'),
]