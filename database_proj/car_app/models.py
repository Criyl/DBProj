from django.db import models

DEFAULT_MAX = 30


class ZipCode(models.Model):
    zip_code = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=DEFAULT_MAX)
    state = models.CharField(max_length=2)


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=DEFAULT_MAX)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.DO_NOTHING)


class Site(models.Model):
    site_id = models.AutoField(primary_key=True)
    site_name = models.CharField(max_length=DEFAULT_MAX)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)


class Salesman(models.Model):
    employee_id = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=DEFAULT_MAX)
    l_name = models.CharField(max_length=DEFAULT_MAX)
    email = models.CharField(max_length=DEFAULT_MAX)
    password = models.CharField(max_length=DEFAULT_MAX)


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=DEFAULT_MAX)
    l_name = models.CharField(max_length=DEFAULT_MAX)
    address_id = models.ForeignKey(Address, blank=True, null=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=DEFAULT_MAX)
    password = models.CharField(max_length=DEFAULT_MAX)


class MakeModel(models.Model):
    mmid = models.AutoField(primary_key=True)
    make = models.CharField(max_length=DEFAULT_MAX)
    model = models.CharField(max_length=DEFAULT_MAX)


class Color(models.Model):
    color_id = models.AutoField(primary_key=True)
    color = models.CharField(max_length=DEFAULT_MAX)


class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    vin = models.CharField(max_length=DEFAULT_MAX)

    mm_id = models.ForeignKey(MakeModel, on_delete=models.DO_NOTHING)
    year = models.IntegerField()
    ticket_price = models.IntegerField()
    mileage = models.IntegerField()
    site_id = models.ForeignKey(Site, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=200)
    img_dir = models.CharField(max_length=DEFAULT_MAX)

    color_id = models.ForeignKey(Color, on_delete=models.DO_NOTHING)


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    employee_id = models.ForeignKey(Salesman, on_delete=models.DO_NOTHING)
    car_id = models.ForeignKey(Car, on_delete=models.DO_NOTHING)


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)


class PotentialSales(models.Model):
    potential_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    inv_id = models.ForeignKey(Inventory, on_delete=models.DO_NOTHING)
    salesman_id = models.ForeignKey(Salesman, blank=True, null=True, on_delete=models.DO_NOTHING)
