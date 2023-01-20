from django.db import models
from django.utils import timezone
# Create your models here.


class Shorturl(models.Model):
    url = models.CharField(max_length=1024)
    surl = models.CharField(max_length=128)
    date = models.DateTimeField(max_length=64, blank=True, default=timezone.now)
    created_user = models.CharField(max_length=64, default='someone')
    def __str__(self):
        return self.surl
