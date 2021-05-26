"""kbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('customers/', views.CustomerListView.as_view(), name='customers'),
    path('customers/<int:pk>', views.CustomerDetailView.as_view(), name='customers-detail'),
    path('customers/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customers-update'),
    path('customers/add/', views.CustomerCreateView.as_view(), name='customers-add'),
    path('sales/', views.SalesListView.as_view(), name='sales'),
    path('sales/add/', views.SalesCreateView.as_view(), name='sales-create'),
    path('sales/<int:pk>', views.SalesDetailView.as_view(), name='sales-detail'),
    path('sales/<int:pk>/update', views.SalesUpdateView.as_view(), name='sales-update'),
    path('delivery-orders/', views.DeliveryOrderListView.as_view(), name='delivery-orders'),
    path('delivery-orders/<int:pk>/detail/', views.DeliveryOrderDetailView.as_view(), name='delivery-order-detail'),
    path('delivery-orders/<int:pk>/edit/', views.DeliveryOrderEditView.as_view(), name='delivery-order-edit'),
    path('delivery-orders/<int:pk>/delete/', views.DeliveryOrderDeleteView.as_view(), name='delivery-order-delete'),
    path('delivery-orders/<int:pk>/delete-product/', views.DeliveryOrderProductDeleteView.as_view(), name='do-product-delete'),
    path('delivery-orders/<int:pk>/edit-product/', views.DeliveryOrderProductEditView.as_view(), name='do-product-edit'),
    path('delivery-orders/create/', views.DeliveryOrderCreateView.as_view(), name='delivery-order-create'),
    path('delivery-orders/<int:pk>/add-product/', views.DeliveryOrderProductAddView.as_view(), name='do-product-add'),
    path('invoices/', views.InvoiceListView.as_view(), name='invoices'),
    path('invoices/<int:pk>/detail', views.InvoiceDetail.as_view(), name='invoice-detail'),
    path('invoices/<int:pk>/print/', views.InvoicePrintNoLogo.as_view(), name='invoice-print'),
    path('invoices/<int:pk>/update', views.InvoiceDetailUpdate.as_view(), name='invoice-update'),
    path('invoice_item/update/', views.update_invoice_item, name="invoice-item-update"),
    path('users/', views.UserListView.as_view(), name="users"),
    path('users/add/', views.UserCreateView.as_view(), name="users-create"),
    path('revenues/', views.RevenueListView.as_view(), name="revenues"),
    path('invoice-report/', views.InvoiceReportListView.as_view(), name="invoice-report"),
    path('categories/', views.CategoryListView.as_view(), name="categories"),
    path('categories/add/', views.CategoryAddView.as_view(), name="categories-add"),
    path('categories/<int:pk>/edit/', views.CategoryEditView.as_view(), name="categories-edit"),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name="categories-delete"),

]
