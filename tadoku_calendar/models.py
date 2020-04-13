import datetime
from django.db import models
from django.utils import timezone
from accounts.models import CustomUser



#class Date(models.Model):
    #date = models.DateField()
    #def __str__(self):
        #return str(self.date)

EVALUATION = [(1, '◎'),(2, '○'),(3, '△'),(4, '×'),]

class Schedule(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=100)
    series = models.CharField(max_length=32)
    level = models.DecimalField(max_digits=2, decimal_places=1)
    word_cnt = models.PositiveIntegerField(default=0)
    evaluation = models.IntegerField(choices=EVALUATION)
    coment = models.CharField(max_length=255)

    def __str__(self):
        return str(self.word_cnt)


