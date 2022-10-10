from django.db import models

# Create your models here.
class senser_log(models.Model):
    recv_sec = models.IntegerField()
    save_hour = models.IntegerField()