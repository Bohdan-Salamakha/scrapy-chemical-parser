from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from parsers.models import ChemicalProduct
from parsers.serializers import NumcasSerializer
from parsers.services.get_average_price_service import GetAveragePriceService


class GetAveragePricePerUnitView(generics.GenericAPIView):
    queryset = ChemicalProduct.objects.all()
    serializer_class = NumcasSerializer

    def get(self, request: Request, *args, **kwargs):
        query_serializer = self.get_serializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)
        chemical_product = get_object_or_404(
            ChemicalProduct, numcas=query_serializer.validated_data.get("numcas")
        )
        average = GetAveragePriceService(chemical_product).get_average()
        return Response({"average": average}, status=status.HTTP_200_OK)
