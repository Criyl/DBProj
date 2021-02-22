# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms


class NewEmployeePage(CreateView):
    form_class = forms.NewEmployeeForm
    success_url = reverse_lazy('')
    template_name = 'employee.html'


class NewPositionPage(CreateView):
    form_class = forms.NewPositionsForm
    success_url = reverse_lazy('home')
    template_name = 'form.html'
