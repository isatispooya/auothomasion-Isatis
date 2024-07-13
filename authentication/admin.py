from django.contrib import admin
from .models import Company, PositionJob, Role, Users, Otp

admin.site.register(Company)
admin.site.register(PositionJob)
admin.site.register(Role)
admin.site.register(Users)
admin.site.register(Otp)
