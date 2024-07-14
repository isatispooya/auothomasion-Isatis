from . import models
from rest_framework import serializers

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = '__all__'

class PositionJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PositionJob
        fields = '__all__'

class RoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'

class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = '__all__'

class OtpSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Otp
        fields = '__all__'