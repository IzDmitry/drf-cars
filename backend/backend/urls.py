from django.urls import path
from cars.views import CarsView, mark_view

urlpatterns = [
    path('update_autoru_catalog/',
         CarsView.as_view(),
         name='update_autoru_catalog'),
    path('', mark_view, name='index'),
]
