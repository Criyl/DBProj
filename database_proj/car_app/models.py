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


class Position(models.Model):
    position_id = models.AutoField(primary_key=True)
    position_name = models.CharField(max_length=DEFAULT_MAX)

    def __str__(self):
        return '%s' % self.position_name


class Salesman(models.Model):
    employee_id = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=DEFAULT_MAX)
    l_name = models.CharField(max_length=DEFAULT_MAX)
    position_id = models.ForeignKey(Position, on_delete=models.DO_NOTHING)
    base_pay = models.FloatField()
    commission = models.FloatField()

    @classmethod
    def create(cls, f, l, p, b, c):
        return cls(f_name=f, l_name=l, position_id=p, base_pay=b, commission=c)


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    f_name = models.CharField(max_length=DEFAULT_MAX)
    l_name = models.CharField(max_length=DEFAULT_MAX)
    address_id = models.ForeignKey(Address, on_delete=models.CASCADE)


class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    make_name = models.CharField(max_length=DEFAULT_MAX)
    model_name = models.CharField(max_length=DEFAULT_MAX)
    year = models.IntegerField()
    color = models.CharField(max_length=DEFAULT_MAX)
    mileage = models.IntegerField()
    description = models.CharField(max_length=200)


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    employee_id = models.ForeignKey(Salesman, on_delete=models.DO_NOTHING)
    car_id = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
