from django.db import models
from django.utils import timezone
# Create your models here.


class Shorturl(models.Model):
    url = models.CharField(max_length=1024)
    surl = models.CharField(max_length=128)
    date = models.DateTimeField(max_length=64, blank=True, default=timezone.now)
    created_user = models.CharField(max_length=64, default='someone')
    click_times = models.IntegerField('访问次数',max_length=1024,default=0)
    def __str__(self):
        return self.surl


class Invitation_code(models.Model):
    code = models.CharField('邀请码', max_length=128)
    timeslimit = models.IntegerField('限制次数', default=1)
    timesused = models.IntegerField('已使用次数', default=0)
    created_user = models.CharField(max_length=64)
    def __str__(self):
        return self.code
