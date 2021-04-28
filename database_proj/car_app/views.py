# Create your views here.
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as oply
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from . import forms
from .models import *


def map_color(color):
    map = {
        "Silver": "",
        "Black": "",
        "Red": "",
        "Blue": "",
    }
    return map.get(color, "")


class CustomerDashView(CreateView):
    form_class = forms.EditCustomerForm
    success_url = reverse_lazy('car_app:customer')
    template_name = 'customer_dashboard.html'


class CatalogView(TemplateView):
    template_name = 'catalog.html'


def piechart_inventory():
    dict = {
        "cars": [],
        "Colors": [],
        "markers": []
    }

    for inv in Inventory.objects.all():
        dict["cars"] += [inv.car_id]
        dict["Colors"] += [inv.car_id.color_id.color]
        dict["markers"] += [inv.car_id.color_id.color]

    df = pd.DataFrame(dict)
    labels = df["Colors"].value_counts().index
    values = df["Colors"].value_counts().values

    # ByColor
    trace = go.Pie(labels=labels, values=values,
                   marker=go.pie.Marker({"colors": df["markers"].values}))
    data = [trace]
    layout = go.Layout(title="Inventory by Color", xaxis={'title': 'x1'}, yaxis={'title': 'x2'})
    fig = go.Figure(data, layout)
    inv_color_plt = oply.plot(fig, auto_open=False, output_type='div')

    # BySold
    dict = {
        "cars": [],
        "Colors": [],
        "markers": []
    }
    for t in Transaction.objects.all():
        dict["cars"] += [t.car_id]
        dict["Colors"] += [t.car_id.color_id.color]
        dict["markers"] += [t.car_id.color_id.color]

    df = pd.DataFrame(dict)
    labels = df["Colors"].value_counts().index
    values = df["Colors"].value_counts().values

    # ByColor
    trace = go.Pie(labels=labels, values=values,
                   marker=go.pie.Marker({"colors": df["markers"].values}))
    data = [trace]
    layout = go.Layout(title="Sold by Color", xaxis={'title': 'x1'}, yaxis={'title': 'x2'})
    fig = go.Figure(data, layout)
    trans_color_plt = oply.plot(fig, auto_open=False, output_type='div')

    return [inv_color_plt, trans_color_plt]


def salesmanView(request):
    context = {
        "cars": Car.objects.all(),
        "dealerships": Site.objects.all(),
        "makemodels": MakeModel.objects.all(),
        "colors": Color.objects.all(),
        "salesman": Salesman.objects.all(),
        "potentials": PotentialSales.objects.all(),
        "transactions": Transaction.objects.all(),
        "charts": [] + piechart_inventory()
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
            for t in Transaction.objects.filter(employee_id=id):
                t.employee_id = 0
            Salesman.objects.filter(employee_id=id).delete()

        if 'SELL' in request.POST:
            potential_id = request.POST.get('potential_id')
            employee_id = request.POST.get('employee_id')

            potential = PotentialSales.objects.filter(potential_id=potential_id).first()

            transaction = Transaction()
            transaction.customer_id = potential.customer_id
            transaction.car_id = potential.inv_id.car_id
            transaction.employee_id = Salesman.objects.filter(employee_id=employee_id).first()
            transaction.save()

            potential.delete()
            potential.inv_id.delete()

        if 'DENY' in request.POST:
            potential_id = request.POST.get('potential_id')
            potential = PotentialSales.objects.filter(potential_id=potential_id)
            potential.delete()

    return render(request, 'salesman_dashboard.html', context)


def catalogView(request):
    context = {
        "customers": Customer.objects.all(),
        "inventory": Inventory.objects.all(),
        "dealerships": Site.objects.all(),
        "makemodels": MakeModel.objects.all(),
        "colors": Color.objects.all()
    }

    if request.method == 'GET':
        print(request.GET)
        if 'ADV_SEARCH' in request.GET:
            if 'mm' in request.GET and request.GET.get('mm'):
                list = request.GET.getlist('mm')
                print(context["inventory"].filter(car_id__mm_id__in=list))
                context["inventory"] = context["inventory"].filter(car_id__mm_id__in=list)

            if 'pricelow' in request.GET and request.GET.get('pricelow'):
                high = request.GET.get('pricelow')
                context["inventory"] = context["inventory"].filter(car_id__ticket_price__gte=high)

            if 'pricehigh' in request.GET and request.GET.get('pricehigh'):
                high = request.GET.get('pricehigh')
                context["inventory"] = context["inventory"].filter(car_id__ticket_price__lte=high)

            if 'milelow' in request.GET and request.GET.get('milelow'):
                high = request.GET.get('milelow')
                context["inventory"] = context["inventory"].filter(car_id__mileage__gte=high)
            if 'milehigh' in request.GET and request.GET.get('milehigh'):
                high = request.GET.get('milehigh')
                context["inventory"] = context["inventory"].filter(car_id__mileage__lte=high)

            if 'colors' in request.GET and request.GET.get('colors'):
                list = request.GET.getlist('colors')
                context["inventory"] = context["inventory"].filter(car_id__color_id__in=list)

            if 'dealership' in request.GET:
                site = request.GET.get('dealership')
                context["inventory"] = context["inventory"].filter(car_id__site_id=site)

    if request.method == 'POST':

        print(request.POST)
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

            if PotentialSales.objects.filter(inv_id__car_id=car_id, customer_id=customer_id).count() == 0:
                potential = PotentialSales()
                potential.inv_id = Inventory.objects.filter(car_id=car_id).first()
                potential.customer_id = Customer.objects.filter(customer_id=customer_id).first()

                potential.save()

        if 'EDIT' in request.POST:
            car_id = request.POST.get('car_id')
            car = Car.objects.filter(car_id=car_id).first()
            if 'edit_mm' in request.POST:
                edit_mmid = request.POST.get('edit_mm')
                car.mm_id = MakeModel.objects.filter(mmid=edit_mmid).first()

            if 'edit_color' in request.POST:
                edit_color = request.POST.get('edit_color')
                car.color_id = Color.objects.filter(color_id=edit_color).first()

            if 'edit_dealership' in request.POST:
                edit_dealership = request.POST.get('edit_dealership')
                car.site_id = Site.objects.filter(site_id=edit_dealership).first()

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

    print(context)

    return render(request, 'catalog.html', context)


def customerView(request):
    context = {
        "customers": Customer.objects.all(),
        "potentials": PotentialSales.objects.all(),
        "transactions": Transaction.objects.all(),

        "cars": Inventory.objects.all(),
        "dealerships": Site.objects.all(),
        "makemodels": MakeModel.objects.all(),
        "colors": Color.objects.all()
    }
    if request.method == 'POST':
        print(request.POST)
        if 'CUSTOMER_EDIT' in request.POST:
            customer_id = request.POST.get("customer_id")
            customer = Customer.objects.filter(customer_id=customer_id).first()

            if "fname" in request.POST and request.POST.get('fname'):
                customer.f_name = request.POST.get("fname")

            if "lname" in request.POST and request.POST.get('lname'):
                customer.l_name = request.POST.get("lname")

            customer.save()

        if 'NEW_CUSTOMER' in request.POST:
            customer = Customer()

            customer.f_name = request.POST.get("customer_fname")
            customer.l_name = request.POST.get("customer_lname")

            customer.email = request.POST.get("customer_email")
            customer.password = request.POST.get("customer_password")

            customer.save()
        if 'DELETE' in request.POST:
            customer_id = request.POST.get('customer_id')
            if Customer.objects.filter(customer_id=customer_id).count() > 0:
                customer = Customer.objects.filter(customer_id=customer_id).first()
                customer.delete()

        if 'REMOVE_POTENTIAL' in request.POST:
            potential_id = request.POST.get('potential_id')

            if PotentialSales.objects.filter(potential_id=potential_id).count() > 0:
                potential = PotentialSales.objects.filter(potential_id=potential_id).first()
                potential.delete()

    return render(request, 'customer_dashboard.html', context)


def loginView(request):
    context = {
        "cars": Inventory.objects.all(),
        "dealerships": Site.objects.all(),
        "makemodels": MakeModel.objects.all(),
        "colors": Color.objects.all()
    }

    return render(request, 'account/login.html', context)
