from django.urls import path

from . import views

app_name = 'car_app'

urlpatterns = [

    path('employee/', views.NewEmployeePage.as_view(), name="employee"),
    path('position/', views.NewPositionPage.as_view(), name="position")
]
