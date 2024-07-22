from django.urls import path
from .views import CaptchaViewest, OtpViewest, LoginViewest, ProfileViewset

urlpatterns = [
    path('captcha/',CaptchaViewest.as_view(),name = 'captcha'),
    path('otp/',OtpViewest.as_view(),name = 'otp'),
    path('login/',LoginViewest.as_view(),name = 'login'),
    path('profile/',ProfileViewset.as_view(), name = 'profile'),

]