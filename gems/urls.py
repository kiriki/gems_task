from django.urls import path

from gems import views

urlpatterns = [
    path('', views.DealsStat.as_view(), name='deals'),
]
