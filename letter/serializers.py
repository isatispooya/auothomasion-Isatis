from . import models
from rest_framework import serializers

class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Letter
        fields = '__all__'
        