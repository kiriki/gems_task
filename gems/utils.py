from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def common_exception_handler(exc, context):
    response = exception_handler(exc, context)

    data = {
        'Status': 'Error',
        'Descr': str(exc) or 'Unknown error',
    }

    if response is not None:
        response.data.update(data)
        return response

    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
