from django.shortcuts import render
from rest_framework.views import APIView
from GuardPyCaptcha.Captch import GuardPyCaptcha
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers
from datetime import datetime, timedelta
from . import fun
import pytz


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

            otp_obj_ = models.Otp.objects.filter(mobile = mobile,code = code)

            otp_obj_ = otp_obj_.order_by('-created_at')
            otp_obj_ = otp_obj_.first()
        except Exception as e:
            return Response({'message':'کد تایید نامعتبر است'})

        otp_obj = serializers.OtpSerializers(otp_obj_).data

        if otp_obj ['code']== None:
            return Response({'message':'کد تایید نامعتبر است'})
    

        now = datetime.now(pytz.UTC)
        delay = now - timedelta(minutes=120)
    
        otp_obj['created_at'] = otp_obj['created_at']
        print(otp_obj)
        date_object = datetime.fromisoformat(otp_obj['created_at'][:-1])
        date_object = date_object.replace(tzinfo=pytz.UTC).timestamp()

        otp_obj['created_at'] = date_object

        if otp_obj['created_at'] <= delay.timestamp():
            otp_obj.delete()
            return Response({'message': 'کد منقضی شده است'}, status=status.HTTP_400_BAD_REQUEST)

        #otp_obj['created_at'] = otp_obj['created_at']
        
        otp_obj_.delete()
        token = fun.encryptionUser(user)

        return Response({'token':token},status=status.HTTP_200_OK)


class ProfileViewset(APIView):
    def get(self,request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'message': 'توکن را وارد کنید'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'message': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = user.first()
        
        profile_data = serializers.UsersSerializers(user).data
        

        return Response(profile_data)