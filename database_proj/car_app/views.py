# Create your views here.
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from . import forms
from .models import *


class CustomerDashView(CreateView):
    form_class = forms.EditCustomerForm
    success_url = reverse_lazy('car_app:customer')
    template_name = 'customer_dashboard.html'


class CatalogView(TemplateView):
    template_name = 'catalog.html'


def salesmanView(request):
    context = {
        "cars": Car.objects.all(),
        "dealerships": Site.objects.all(),
        "makemodels": MakeModel.objects.all(),
        "colors": Color.objects.all(),
        "salesman": Salesman.objects.all(),
        "potentials": PotentialSales.objects.all(),
        "transactions": Transaction.objects.all()
    }
    if request.method == 'POST':
        print(request.POST)
        if 'SALESMAN' in request.POST:
            salesman = Salesman()
            salesman.f_name = request.POST.get('salesman_fname')
            salesman.l_name = request.POST.get('salesman_lname')
            salesman.email = request.POST.get('salesman_email')
            salesman.password = request.POST.get('salesman_password')
            salesman.save()
        if 'DELETE' in request.POST:
            id = request.POST.get('salesman_id')
            print(id)
            print(Salesman.objects.filter(employee_id=id))
            Salesman.objects.filter(employee_id=id).delete()

        if 'SELL' in request.POST:
            potential_id = request.POST.get('potential_id')
            employee_id = request.POST.get('employee_id')

            potential = PotentialSales.objects.filter(potential_id=potential_id).first()

            transaction = Transaction()
            transaction.customer_id = potential.customer_id
            transaction.car_id = potential.car_id
            transaction.employee_id = Salesman.objects.filter(employee_id=employee_id).first()
            transaction.save()

            inv = Inventory.objects.filter(car_id=potential.car_id).first()
            inv.delete()
            potential.delete()

        if 'DENY' in request.POST:
            potential_id = request.POST.get('potential_id')
            potential = PotentialSales.objects.filter(potential_id=potential_id)
            potential.delete()

    return render(request, 'salesman_dashboard.html', context)


def catalogView(request):
    context = {
        "cars": Inventory.objects.all(),
        "dealerships": Site.objects.all(),
        "makemodels": MakeModel.objects.all(),
        "colors": Color.objects.all()
    }

    if request.method == 'POST':
        if 'CAR' in request.POST:
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

            inventory = Inventory()
            inventory.car_id = car
            inventory.save()

        if 'MM' in request.POST:
            mm = MakeModel()

            mm.make = request.POST.get('add_make')
            mm.model = request.POST.get('add_model')

            mm.save()

        if 'COLOR' in request.POST:
            c = Color()
            c.color = request.POST.get('add_new_color')
            c.save()

        if 'DEALERSHIP' in request.POST:
            zipcode = ZipCode()
            zipcode.zip_code = request.POST.get('dealership_zipcode')
            zipcode.city = request.POST.get('dealership_city')
            zipcode.state = request.POST.get('dealership_state')
            zipcode.save()

            addr = Address()
            addr.street_number = request.POST.get('dealership_st_num')
            addr.street_name = request.POST.get('dealership_st_name')
            addr.zip_code = ZipCode.objects.filter(zip_code=request.POST.get('dealership_zipcode')).first()
            addr.save()

            dealership = Site()
            dealership.site_name = request.POST.get('dealership_name')
            dealership.address_id = Address.objects.filter(address_id=addr.address_id).first()
            dealership.save()

        if 'BUY' in request.POST:
            car_id = request.POST.get('car_id')
            customer_id = request.POST.get('customer_id')
            if PotentialSales.objects.filter(car_id=car_id, customer_id=customer_id).count() == 0:
                potential = PotentialSales()
                potential.car_id = Car.objects.filter(car_id=car_id).first()
                potential.customer_id = Customer.objects.filter(customer_id=customer_id).first()

                potential.save()

        if 'EDIT' in request.POST:
            car_id = request.POST.get('car_id')
            car = Car.objects.filter(car_id=car_id).first()
            car.vin = request.POST.get('edit_vin')
            car.year = request.POST.get('edit_year')
            car.price = request.POST.get('edit_price')
            car.mileage = request.POST.get('edit_mile')
            car.description = request.POST.get('edit_description')
            car.save()

        if 'DELETE_CAR' in request.POST:
            car_id = request.POST.get('car_id')
            if Car.objects.filter(car_id=car_id).count() > 0:
                car = Car.objects.filter(car_id=car_id).first()
                car.delete()

    return render(request, 'catalog.html', context)
