from django.urls import path

from . import views

app_name = 'car_app'

urlpatterns = [
    path('customer', views.CustomerDashView.as_view(), name="customer"),
    path('catalog', views.catalogView, name="catalog"),
    path('car_manager', views.SalespersonDashView.as_view(), name="car_manager"),
    path('employee/', views.NewEmployeePage.as_view(), name="employee"),
    path('position/', views.NewPositionPage.as_view(), name="position"),
]
