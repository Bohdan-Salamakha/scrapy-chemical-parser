from rest_framework import serializers

from parsers.models import ChemicalProduct


class ChemicalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemicalProduct
        fields = "__all__"


class ScrapeSiteSerializer(serializers.Serializer):
    company_name = serializers.ChoiceField(
        choices=[
            "accelpharmtech"
        ]
    )
