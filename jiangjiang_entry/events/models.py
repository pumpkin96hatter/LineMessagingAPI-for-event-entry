from django.db import models
from django.utils import timezone


# Create your models here.

class Schedule(models.Model):
    schedule_url = models.CharField(max_length=300, null=True, default='')

    def __str__(self):
        return self.schedule_url
    
class Entry(models.Model):
    name = models.CharField(max_length=30, null=True, default='')

    def __str__(self):
        return self.name

class Participant(models.Model):
    participant = models.CharField(max_length=50, null=True, default='')#useridのこと
     
    def __str__(self):
        return f'{self.participant[:40]}'
    

class Line_Name(models.Model):
    line_name = models.CharField(max_length=40, default='')
    participant = models.ForeignKey(to=Participant, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.line_name

    
class Event_Type(models.Model):
    type_name = models.CharField(max_length=15, default='')
    event_date =models.DateTimeField(default=timezone.now) 
    pic_url = models.CharField(max_length=300, default='')
    
    def __str__(self):
        return  f'{self.event_date}:{self.type_name[:15]}'


    
class Application_Info(models.Model):
    """
     status
        0: 未エントリー
        1: エントリー完了
        2: キャンセル
        3: 
    """
    status = models.SmallIntegerField(default=0) 
    applied_at = models.DateTimeField(null=True, default=timezone.now)
    participant = models.ForeignKey(to=Participant, null=True, on_delete=models.CASCADE)
    event_type = models.ForeignKey(to=Event_Type, null=True, on_delete=models.CASCADE)
    entry = models.ForeignKey(to=Entry, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.applied_at}'

#キャンセルの時考慮 
# class Application_Log(models.Model):
#     entry = models.ManyToManyField(Entry, blank=True)
#     amount = models.SmallIntegerField(blank=True, null=True, default=1)
#     applied_at = models.DateTimeField(default=timezone.now)
#     application_info = models.ForeignKey(to=Application_Info, on_delete=models.CASCADE)
#     # event_type = models.ForeignKey(to=Event_Type, on_delete=models.CASCADE)

