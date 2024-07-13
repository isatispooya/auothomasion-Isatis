from . import models
from rest_framework import serializers

class CompanySerializer(serializers.ModelSerializers):
    class Meta:
        model = models.Company
        fields = '__all__'

class PositionJobSerializer(serializers.ModelSerializers):
    class Meta:
        model = models.PositionJob
        fields = '__all__'

class RoleSerializers(serializers.ModelSerializers):
    class Meta:
        model = models.Role
        fields = '__all__'

class UsersSerializers(serializers.ModelSerializers):
    class Meta:
        model = models.Users
        fields = '__all__'

class OtpSerializers(serializers.ModelSerializers):
    class Meta:
        model = models.Otp
        fields = '__all__'