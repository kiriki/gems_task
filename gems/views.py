from rest_framework import viewsets
from rest_framework.response import Response

from django.db.models import Sum

from gems.models import Customer
from gems.serializers import CustomerSerializer


class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.annotate(
        spent_money=Sum('deal__total')
    ).order_by('-spent_money')[:5]

    serializer_class = CustomerSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'response': serializer.data})
