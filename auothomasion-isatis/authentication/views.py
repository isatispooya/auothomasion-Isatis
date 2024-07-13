from django.shortcuts import render
from rest_framework.views import APIView
from GuardPyCaptcha.Captch import GuardPyCaptcha
from rest_framework.response import Response
from rest_framework import status
from . import models


class CaptchaViewest(APIView):
    def get (self,request):
        captcha = GuardPyCaptcha()
        captcha = captcha.Captcha_generation(num_char=4,only_num=True)
        return Response(captcha,status=status.HTTP_200_OK)

class OtpViewest(APIView):
    def post(self,request):
        captcha = GuardPyCaptcha()
        captcha = captcha.check_response(request.data['encrypted_response'],request.data['captcha'])
        if False:#not captcha:
            result = {'message':'کد کپچا صحیح نمی باشد'}
            return Response(result,status=status.HTTP_406_NOT_ACCEPTABLE)
        national_code = request.data['national_code']
        if not national_code:
            result = {'message':'کدملی لازم است'}
            return Response(result,status=status.HTTP_400_BAD_REQUEST)
        
        try:
            users = models.Users.objects.get(national_code=national_code)
            otp = '11111'
            otp_obj = models.Otp(code=otp,mobile=users.mobile)
            otp_obj.save()
            result = {'message':'کد تایید ارسال شد'}
            return Response(result,status=status.HTTP_200_OK)   
        except models.Users.DoesNotExist:
            result = {'message':'کاربر یافت نشد'}
            return Response(result,status=status.HTTP_401_UNAUTHORIZED)   
  
    
    
