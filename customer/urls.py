from django.urls import path

from customer.views.auth import logout_page, LoginView, RegisterFormView
from customer.views.customers import customers_page, add_customer, delete_customer, edit_customer, export_data, \
    SendMailView

urlpatterns = [
    path('customer-list/', customers_page, name='customers'),
    path('add-customer/', add_customer, name='add_customer'),
    path('customer/<int:pk>/delete', delete_customer, name='delete'),
    path('customer/<int:pk>/update', edit_customer, name='edit'),
    # Authentication path
    path('login-page/', LoginView.as_view(), name='login'),
    path('logout-page/', logout_page, name='logout'),
    path('register-page/', RegisterFormView.as_view(), name='register'),
    path('export-data/', export_data, name='export_data'),
    path('send-mail/', SendMailView.as_view(), name='send_mail'),
]
