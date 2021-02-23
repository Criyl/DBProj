from django.urls import path

from . import views

app_name = 'car_app'

urlpatterns = [

    path('employee/', views.NewEmployeeView.as_view(), name="employee"),
    path('position/', views.NewPositionView.as_view(), name="position"),
    path('make/', views.NewMakeView.as_view(), name="make"),
    path('model/', views.NewModelView.as_view(), name="model"),
    path('newcar/', views.NewCarView.as_view(), name="newcar"),
    path('site/', views.createSiteForm, name="site")
]
