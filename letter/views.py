from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models
from authentication.models import PositionJob, Users, Company 
from authentication.serializers import PositionJobSerializer
from letter.serializers import LetterSerializer
from . import serializers
from authentication import fun
from datetime import datetime
from persiantools.jdatetime import JalaliDate
from datetime import datetime
from random import randint
#from django.db.models import Count
from letter.models import Letter
from persiantools.jdatetime import JalaliDate



def receiver():
    receivers = PositionJob.objects.all()
    receivers_serializer  = PositionJobSerializer(receivers, many =True).data
    for i in receivers_serializer:
        item_user = Users.objects.get(id = i['user'])
        i['user'] = item_user.firstname + ' ' + item_user.lastname+ ' ['+ item_user.national_code+ ']'
        item_company = Company.objects.get(id = i['company'])
        i['company'] = item_company.name
    return receivers_serializer


def generate_number_letters():
    current_date = datetime.now()
    jalali_date = JalaliDate(current_date.date())
    year = jalali_date.year

    
    letters = Letter.objects.filter(year=current_date.year)
    total_letters = letters.count()

    random_index = randint(0, 9)
    letter_num = f'د/{year}/{random_index}{total_letters + 1}'

    return letter_num

#لیست گیرنده ها را به ما می دهد
class ReceiverViewset(APIView):
    def get(self,request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'message': 'توکن احراز هویت موجود نیست'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'message': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
            
        recieve =receiver()


        return Response(recieve, status=status.HTTP_200_OK)

class SenderViewset(APIView):
    def get(self,request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'message': 'توکن احراز هویت موجود نیست'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user :
            return Response({'message': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        user = user.first()
        sender = PositionJob.objects.filter(user = user)
        sender_serializer  = PositionJobSerializer(sender, many =True).data
        for i in sender_serializer:
            item_user = Users.objects.get(id = i['user'])
            i['user'] = item_user.firstname + ' ' + item_user.lastname+ ' ['+ item_user.national_code+ ']'
            item_company = Company.objects.get(id = i['company'])
            i['company'] = item_company.name 

        return Response(sender_serializer, status=status.HTTP_200_OK)
    
#ایجاد نامه
class CreateletterViewset(APIView):
    
    def post(self,request):
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'message': 'توکن احراز هویت موجود نیست'}, status=status.HTTP_400_BAD_REQUEST)
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'message': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        
        receiver_id = request.data['receiver']
        sender_id = request.data['sender']
        subject = request.data['subject']
        text = request.data['text']
        date = request.data['date']
    

        if not date:
            return Response({'message': 'تاریخ ارسال نشده است'}, status=status.HTTP_400_BAD_REQUEST)

        try:
        
            g_date = datetime.fromtimestamp(date)
            jalali_date = JalaliDate(g_date)

            year = jalali_date.year

        except ValueError:
            return Response({'message': 'تاریخ نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            receiver = PositionJob.objects.get(id=receiver_id)
            sender = PositionJob.objects.get(id=sender_id)
        except:
            return Response({'message': 'گیرنده یا فرستنده یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)

        letter_number = generate_number_letters()


        letter = models.Letter(receiver=receiver,sender=sender,subject=subject,text=text,date=g_date,year = year, letter_number = letter_number)
        serializer = LetterSerializer(data=letter)
        # print(serializer.)
        # if not serializer.is_valid():
        #     return Response({'message':'خطا'},status=status.HTTP_400_BAD_REQUEST)
        letter.save()
        return Response({'message': 'نامه با موفقیت ایجاد شد'} ,status=status.HTTP_201_CREATED)
    

#مشخصات یک نامه را می فرستد    
class DetailletterViewset(APIView):
    def get (self, request,id):
        
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'message': 'توکن احراز هویت موجود نیست'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = fun.decryptionUser(Authorization)
        if not user:
            return Response({'message': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            letter = models.Letter.objects.get(id=id)
        except models.Letter.DoesNotExist:
            return Response({'message': 'نامه مورد نظر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
        
        
        serializer = LetterSerializer(letter)
        return Response(serializer.data, status=status.HTTP_200_OK)

# نامه های ارسال شده توسط کاربر را بهش نشان بدهد
class BoxletterViewset(APIView):
    def get(self,request): 
        Authorization = request.headers.get('Authorization')
        if not Authorization:
            return Response({'message': 'توکن احراز هویت موجود نیست'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = fun.decryptionUser(Authorization)
      
        if not user:
            return Response({'message': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)
        user_instance = user.first()
        
        print(user_instance)

        #position_jobs = PositionJob.objects.filter(user=user_instance)

        letters = Letter.objects.filter(receiver = user_instance)
        print(letters)

        serializer = LetterSerializer(letters, many =True)
        
        print(serializer)
        

        return Response(serializer.data, status=status.HTTP_200_OK)
    

