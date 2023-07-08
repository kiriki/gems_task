from django.urls import path

from gems import views

DEALS_VIEW_NAME = 'deals'

urlpatterns = [
    path('', views.DealsStat.as_view(), name=DEALS_VIEW_NAME),
]
