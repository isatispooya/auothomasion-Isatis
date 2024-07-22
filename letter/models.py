from django.db import models
from authentication.models import PositionJob
import datetime
class Attachment(models.Model):
    file = models.FileField(upload_to='statics/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.file}'

class Letter(models.Model):
    receiver = models.ForeignKey(PositionJob,on_delete= models.CASCADE, related_name= 'receiver')
    sender = models.ForeignKey(PositionJob,on_delete= models.CASCADE,related_name='sender')
    subject = models.TextField(max_length=200)
    text = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    year = models.IntegerField()
    seen = models.BooleanField(default=False)
    letter_number = models.CharField(max_length=15,unique=True)
    attachment = models.ManyToManyField(Attachment, related_name='attachment',null = True, blank= True)

    def __str__(self):
        return f'{self.letter_number}'
    
