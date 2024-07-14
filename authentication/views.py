from django.shortcuts import render
from rest_framework.views import APIView
from GuardPyCaptcha.Captch import GuardPyCaptcha
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
import datetime 
from . import fun


class CaptchaViewest(APIView):
    def get (self,request):
        captcha = GuardPyCaptcha()
        captcha = captcha.Captcha_generation(num_char=4,only_num=True)
        return Response(captcha,status=status.HTTP_200_OK)

class OtpViewest(APIView):
    def post(self,request):
        captcha = GuardPyCaptcha()
        print(request.data)
        #captcha = captcha.check_response(request.data['encrypted_response'],request.data['captcha'])
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
  
class LoginViewest(APIView):
    def post(self,request):
        national_code = request.data.get('national_code')
        code = request.data.get('code')  

        if not national_code or not code:
            return Response({'message': 'کد ملی و کد تایید لازم است'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = models.Users.objects.get(national_code=national_code)
        if not user:
            return Response({'message':'کد ملی موجود نیست لطفا ثبت نام کنید'})
        try:

            mobile = user.mobile
            otp_obj = models.Otp.objects.filter(mobile = mobile,code = code).order_by('-date').first()
        except:
            return Response({'message':'کد تایید نامعتبر است'})

        otp_obj = serializers.OtpSerializers(otp_obj).data

        if otp_obj ['code']== None:
            return Response({'message':'کد تایید نامعتبر است'})
    
        now = datetime.datetime.now()
        deley = now-datetime.timedelta(minutes=120)
        if otp_obj.date.timestamp()<=deley.timestamp():
            result = {'message':'کد منقضی شده است'}
            otp_obj.delete()
            return Response(result,status=status.HTTP_400_BAD_REQUEST)
        otp_obj.delete()
        user = user.first()
        token = fun.encryptionUser(user)

        return Response({'token':token},status=status.HTTP_200_OK)

