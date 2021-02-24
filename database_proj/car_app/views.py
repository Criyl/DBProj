# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from . import forms


class NewEmployeePage(CreateView):
    form_class = forms.NewEmployeeForm
    success_url = reverse_lazy('')
    template_name = 'employee.html'


class NewPositionPage(CreateView):
    form_class = forms.NewPositionsForm
    success_url = reverse_lazy('home')
    template_name = 'form.html'


class CustomerDashView(CreateView):
    form_class = forms.EditCustomerForm
    success_url = reverse_lazy('car_app:customer')
    template_name = 'customer_dashboard.html'


class TV(TemplateView):
    template_name = 'customer_dashboard.html'
