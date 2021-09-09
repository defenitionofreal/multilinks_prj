from rest_framework import serializers
from .models import *

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateBlock
        fields = ("user", "name", "close", "order")