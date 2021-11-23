from django.db import models
from django.utils import timezone


# Create your models here.
class Event_Type(models.Model):
    name = models.CharField(max_length=15)
    # image = models.ImageField(upload_to='images', blank=True,  null=True, default=None)
    
    def __str__(self):
        return self.name

    
class Entry(models.Model):
    event_type = models.ForeignKey(Event_Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
 
class Application_Info(models.Model):
    """
    status
        0: 未エントリー
        1: エントリー完了
        2: 参加確定
        3: 参加連絡済み
    """
    participant = models.CharField(max_length=50)
    applied_at = models.DateTimeField(default=timezone.now)
    status = models.SmallIntegerField(default=0)
    
    def __str__(self):
        return f'{self.participant[:40]}:{self.applied_at}'

class Application_Log(models.Model):
    entry = models.ForeignKey(to=Entry, null=True, on_delete=models.SET_NULL)
    amount = models.SmallIntegerField()
    application_info = models.ForeignKey(to=Application_Info, on_delete=models.CASCADE)

