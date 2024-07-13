from django.urls import path
from .views import CaptchaViewest, OtpViewest

urlpatterns = [
    path('captcha/',CaptchaViewest.as_view(),name = 'captcha'),
    path('otp/',OtpViewest.as_view(),name = 'otp'),

]