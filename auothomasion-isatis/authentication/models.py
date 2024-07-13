from django.db import models
from django.utils.timezone import now
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    national_code = models.CharField(max_length=200,unique=True)
    subject = models.CharField(max_length=200)
    TYPE_CHOICES = [('s','سهامی خاص'),('g','سهامی عام')]
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    email = models.EmailField(blank=True, null=True,unique=True )
    address= models.CharField(max_length=800)
    site = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.name}'

class PositionJob(models.Model):
    name = models.CharField(max_length=200)
    level = models.CharField(max_length=200)
   
    def __str__(self):
        return f'{self.name}'


class Role(models.Model):
    title_choice =[('s','سهامدار'),('c','مشتری'),('e','کارمند')]
    title =models.CharField(max_length=1,choices = title_choice)
    
    def __str__(self):
        return f'{self.title}'


class Users(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    national_code = models.CharField(max_length=200,unique=True)
    mobile = models.CharField(max_length=200,unique=True)
    profile_picture = models.ImageField(upload_to = 'static/image/',blank = True, null = True)
    date_birth=models.DateTimeField(blank=True, null=True)
    personel = models.BooleanField(default=False)
    job = models.ForeignKey(PositionJob,on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    
class Otp(models.Model):
    mobile = models.CharField(max_length=200)
    code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return f'{self.code}'