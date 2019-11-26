from django.urls import path

from .views import homePageView, readPlateNumber

urlpatterns = [
    path('', homePageView, name='home'),
    path('getPlateNumber/<str:imageName>/', readPlateNumber, name='readPlateNumber'),
]