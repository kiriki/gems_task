from rest_framework.routers import DefaultRouter

from django.urls import include, path

from gems import views

router = DefaultRouter()

router.register('customers', views.CustomersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
