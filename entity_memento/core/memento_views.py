from .models import *

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as status_codes

from .utils import get_filter_params


class MementoManagement(APIView):
    Model = None
    def get(self, request, *args, **kwargs):
        params = request.query_params
        filter_params = get_filter_params(params)

        if filter_params:
            data = self.Model.objects.filter(**filter_params)
        else:
            data = self.Model.objects.all()

        paginate_data = self.paginate_queryset(data, request, calculate_count=False, view=self, ordering_field="-modification_date")
        data = paginate_data.values()
        return Response({"data" : data, "STATUS" : "SUCCESS"}, status=status_codes.HTTP_200_OK)


class ProductManagement(MementoManagement):
    Model = ProductMemento
