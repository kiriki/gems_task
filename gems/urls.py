from django.urls import path
from django.views.decorators.cache import cache_page

from gems import views

DEALS_VIEW_NAME = 'deals'
ONE_DAY = 60 * 60 * 24

urlpatterns = [
    path(
        '', cache_page(timeout=ONE_DAY)(views.DealsStat.as_view()), name=DEALS_VIEW_NAME
    ),
]
