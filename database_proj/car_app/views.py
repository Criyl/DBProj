# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from . import forms
from .models import *


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


class SalespersonDashView(TemplateView):
    template_name = 'car_manager.html'


class CatalogView(TemplateView):
    template_name = 'catalog.html'


def catalogView(request):
    context = {
        "cars": Car.objects.all(),
        "dealerships": Site.objects.all(),
        "makemodels": MakeModel.objects.all(),
        "colors": Color.objects.all()
    }
    print("catalog... %s" % request.method)
    if request.method == 'POST':
        print("CAR REQUEST")
        print("post: %s" % request.POST)
        print("VIN: %s" % request.POST.get('add_vin'))
        car = Car()
        car.vin = request.POST.get('add_vin')
        car.year = request.POST.get('add_year')
        car.ticket_price = request.POST.get('add_price')
        car.mileage = request.POST.get('add_mile')
        car.description = request.POST.get('add_description')
        car.img_dir = "/0000"

        car.mm_id = MakeModel.objects.filter(mmid=request.POST.get('add_mm')).first()
        car.color_id = Color.objects.filter(color_id=request.POST.get('add_color')).first()
        car.site_id = Site.objects.filter(site_id=request.POST.get('add_dealership')).first()

        car.save()
        return render(request, 'catalog.html', context)

    return render(request, 'catalog.html', context)
