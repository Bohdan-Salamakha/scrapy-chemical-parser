from rest_framework import serializers

from parsers.models import ChemicalProduct


class ChemicalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemicalProduct
        fields = "__all__"


class NumcasSerializer(serializers.Serializer):
    numcas = serializers.CharField()
