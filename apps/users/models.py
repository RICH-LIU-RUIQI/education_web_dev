from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class BaseModel(models.Model):
    add_time = models.DateTimeField(verbose_name='data add time', default=datetime.now)  # not method

    class Meta:
        abstract = True


class UserProfile(AbstractUser):
    nick_name = models.CharField(verbose_name='client nickname', max_length=50, default='')
    birthday = models.DateField(verbose_name='birthday', null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("m", "male"), ("f", "female")), default="f")
    address = models.CharField(max_length=100, default="address")
    mobile = models.CharField(max_length=11, null=True, blank=True)  # 不要设update = true
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100)

    class Meta:
        verbose_name = 'client information'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username






