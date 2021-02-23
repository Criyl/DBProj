# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *


class NewEmployeeView(CreateView):
    form_class = forms.NewEmployeeForm
    success_url = reverse_lazy('')
    template_name = 'employee.html'


class NewPositionView(CreateView):
    form_class = forms.NewPositionsForm
    success_url = reverse_lazy('home')
    template_name = 'form.html'


class NewCarView(CreateView):
    form_class = forms.NewCarForm
    success_url = reverse_lazy('home')
    template_name = 'newcar.html'


class NewMakeView(CreateView):
    form_class = forms.NewMakeForm
    success_url = reverse_lazy('car_app:newcar')
    template_name = 'form.html'


class NewModelView(CreateView):
    form_class = forms.NewModelForm
    success_url = reverse_lazy('car_app:newcar')
    template_name = 'form.html'


class NewSiteView(CreateView):
    form_class = forms.NewSiteForm
    success_url = reverse_lazy('home')
    template_name = 'form.html'


def createSiteForm(request):
    if request.method == 'POST':
        forms = [SiteForm(request.POST),
                 AddressForm(request.POST),
                 ZipCodeForm(request.POST)]
        valid = True
        for form in forms:
            if not form.is_valid():
                valid = False
        if (valid):
            for form in forms:
                form.save()
            return render(request, "{% url 'home' %})")
    else:
        return render(request, 'form.html')
