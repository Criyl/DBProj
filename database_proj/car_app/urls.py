from django.urls import path

from . import views

app_name = 'car_app'

urlpatterns = [
    path('customer', views.customerView, name="customer"),
    path('catalog', views.catalogView, name="catalog"),
    path('salesman', views.salesmanView, name="salesman"),

    path('login/', views.loginView, name="login")
]
