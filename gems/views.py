from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from gems.serializers import (
    CustomerSerializer,
    DealsFileUploadSerializer,
    selected_customers_queryset,
)


class DealsStat(GenericAPIView):
    queryset = selected_customers_queryset

    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'response': serializer.data})

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            r = serializer.save()

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {
                    'Status': 'Error',
                    'Descr': str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(r, status=status.HTTP_200_OK)

    def get_serializer_class(self) -> type[BaseSerializer]:
        if self.request.method == 'POST':
            return DealsFileUploadSerializer
        return CustomerSerializer
