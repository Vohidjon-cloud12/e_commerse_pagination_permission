from django.contrib import admin
from django.urls import path, include
from app.views import  ProductDetailTemplateView, AddProductView, ProductListView


urlpatterns = [
    path('index/',  ProductListView.as_view(), name='index'),
    path('product-detail/<int:product_id>', ProductDetailTemplateView.as_view, name='product_detail'),
    path('add-product/', AddProductView.as_view, name='add_product')
]
