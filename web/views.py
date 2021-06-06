from django.shortcuts import render, reverse, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm
import json
from .models import Customer, Sales, Category, DeliveryOrder, Product, Invoice, InvoiceItem
import datetime
from .filters import InvoiceFilter

# Create your views here.

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    paginate_by = 20

class CustomerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Customer
    fields = '__all__'
    success_url = '/customers/'
    success_message = "Customer has been added successfully"

class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer

class CustomerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Customer
    fields = '__all__'
    success_message = "Customer has been updated"

    def get_success_url(self):
        return reverse_lazy('customers-detail', kwargs={'pk':self.kwargs['pk']})

class CustomerDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Customer
    success_message = "Customer has been deleted"
    success_url = '/customers/'

class SalesCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Sales
    fields = '__all__'
    success_url = '/sales/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['starting_date'].widget = forms.DateInput(attrs={"data-toggle":"date-picker",  "data-single-date-picker":"true"}, format='%d/%m/%Y')
        form.fields['starting_date'].input_formats = ['%d/%m/%Y']
        return form 

class SalesListView(LoginRequiredMixin, ListView):
    model = Sales
    paginate_by = 20

class SalesDetailView(LoginRequiredMixin, DetailView):
    model = Sales

class SalesUpdateView(LoginRequiredMixin, UpdateView):
    model = Sales
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('sales-detail', kwargs={'pk':self.kwargs['pk']})

class SalesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Sales
    fields = '__all__'
    success_message = "Sales has been updated"

    def get_success_url(self):
        return reverse_lazy('sales-detail', kwargs={'pk':self.kwargs['pk']})
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['starting_date'].widget = forms.DateInput(attrs={"data-toggle":"date-picker", "data-single-date-picker":"true", "value":self.object.starting_date}, format='%d/%m/%Y')
        form.fields['starting_date'].input_formats = ['%d/%m/%Y']

        return form 

class SalesDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Sales
    success_message = "Sales telah berhasil dihapus"
    success_url = '/sales/'

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category

class CategoryAddView(LoginRequiredMixin, CreateView):
    model = Category
    success_url = '/categories/'
    fields = '__all__'

class CategoryEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    success_url = '/categories/'
    fields = '__all__'
    success_message = 'Kategori berhasil diupdate'

class CategoryDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Category
    success_url = '/categories/'
    success_message = 'Kategori berhasil dihapus'

class DeliveryOrderCreateView(LoginRequiredMixin, CreateView):
    model = DeliveryOrder
    fields = '__all__' 

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['delivery_order_date'].widget = forms.DateInput(attrs={"data-toggle":"date-picker", "data-single-date-picker":"true"}, format='%d/%m/%Y')
        form.fields['delivery_order_date'].input_formats = ['%d/%m/%Y']
        form.fields['added_by'].widget = forms.HiddenInput(attrs={'value':self.request.user.id})

        return form 
    
    def get_success_url(self):
        return reverse_lazy('do-product-add', kwargs={'pk':self.object.id})

class DeliveryOrderListView(LoginRequiredMixin, ListView):
    model = DeliveryOrder
    paginate_by = 20

class DeliveryOrderDetailView(LoginRequiredMixin, DetailView):
    model = DeliveryOrder

class DeliveryOrderDeleteView(LoginRequiredMixin, DeleteView):
    model = DeliveryOrder
    success_url = '/delivery-orders/'

class DeliveryOrderEditView(LoginRequiredMixin, UpdateView):
    model = DeliveryOrder
    fields = ['customer', 'sales', 'delivery_order_date', 'pic']

    def get_success_url(self, **kwargs):
        return reverse_lazy('delivery-order-detail', kwargs={'pk':self.kwargs['pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mode"] = 'Update' 
        return context

class DeliveryOrderProductAddView(LoginRequiredMixin, CreateView):
    model = Product
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['delivery_order'].widget = forms.HiddenInput(attrs={'value':self.kwargs['pk']})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delivery_order"] = DeliveryOrder.objects.get(id=self.kwargs['pk'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('do-product-add', kwargs={'pk':self.kwargs['pk']})

class DeliveryOrderProductEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    fields = '__all__'
    success_message = "Produk telah berhasil diupdate."

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['delivery_order'].widget = forms.HiddenInput(attrs={'value':self.kwargs['pk']})
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["delivery_order"] = DeliveryOrder.objects.get(id=self.object.delivery_order.id)
        return context
    
    def get_success_url(self):
        return reverse_lazy('delivery-order-detail', kwargs={'pk':self.object.delivery_order.id})


class DeliveryOrderProductDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('delivery-order-detail', kwargs={'pk':self.object.delivery_order.id})

class DeliveryOrderPrintView(LoginRequiredMixin, DetailView):
    model = model = DeliveryOrder
    template_name = 'web/deliveryorder_print.html'

class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice 
    paginate_by = 20

class InvoiceDetail(LoginRequiredMixin, DetailView):
    model = Invoice

class InvoicePrintNoLogo(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'web/invoice_print_nologo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = self.request.GET.get('logo')
        return context

class InvoiceDetailUpdate(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'web/invoice_form_update.html'

    def post(self, request, pk):
        if request.method == 'POST':
            discount = request.POST.get('discount')
            sales_tax = request.POST.get('sales-tax')
            total = request.POST.get('total')
            print(total)
            delivery_cost = request.POST.get('delivery-cost')
            rounded = request.POST.get('rounded')
            try:
                invoice = Invoice.objects.get(id=self.kwargs['pk'])
                invoice.discount = discount
                invoice.sales_tax = sales_tax
                invoice.total = total
                invoice.delivery_cost = delivery_cost
                invoice.rounded = rounded
                invoice.save()
                messages.success(request, "Faktur telah berhasil diupdate")
                return HttpResponseRedirect(reverse('invoice-detail', kwargs={'pk':self.kwargs['pk']}))
            except Exception as error:
                print(error)
                return render(request, 'invoice_detail.html')


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'web/user_list.html'

class UserCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'web/user_form.html'

    def get(self, request):
        form = UserForm
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users'))

class RevenueListView(LoginRequiredMixin, ListView):
    model = Invoice
    paginate_by = 20 
    template_name = 'web/revenue_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get('date-range'):
            date_range = self.request.GET.get('date-range').split(' - ')
            queryset = queryset.filter(created__range=date_range)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = InvoiceFilter(self.request.GET, queryset=self.get_queryset())
        return context

class InvoiceReportListView(LoginRequiredMixin, ListView):
    model = Invoice
    paginate_by = 20
    template_name = 'web/invoice_report_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.GET.get('date-range'):
            date_range = self.request.GET.get('date-range').split(' - ')
            queryset = queryset.filter(created__range=date_range)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = InvoiceFilter(self.request.GET, queryset=self.get_queryset())
        return context


def update_invoice_item(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        unit_price = request.POST.get('unit_price')
        discount = request.POST.get('discount')

        invoice_item = InvoiceItem.objects.get(id=id)
        if unit_price:
            invoice_item.unit_price = unit_price
        
        if discount:
            invoice_item.discount = discount
        
        invoice_item.save()

        response_data = {
            'result': 'successfully updated',
            
        }

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

def update_invoice(request):
    if request.method == "POST":
        id = request.POST.get('id')
        total = request.POST.get('total')
        delivery_cost = request.POST.get('delivery_cost')
        rounded = request.POST.get('rounded-total')

