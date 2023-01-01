# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
# from DjangoUeditor.models import UEditorField
from django.contrib.auth import get_user_model

from apps.users.models import BaseModel
# from apps.courses.models import Course

# Create your models here.
UserProfile = get_user_model()  # get from setting


class CityDict(BaseModel):
    name = models.CharField(max_length=20, verbose_name="city")
    desc = models.CharField(max_length=200, verbose_name="desp")

    class Meta:
        verbose_name = "org city"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(BaseModel):
    name = models.CharField(max_length=50, verbose_name="org name")
    desc = models.TextField(verbose_name='description of org')
    tag = models.CharField(default="country known", max_length=10, verbose_name="organization")
    category = models.CharField(default="pxjg", verbose_name=u"organization category", max_length=20,
                                choices=(("pxjg","organization"),("gr","personal"),("gx","college")))
    click_nums = models.IntegerField(default=0, verbose_name=u"click")
    fav_nums = models.IntegerField(default=0, verbose_name=u"favor")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name=u"organization address")
    city = models.ForeignKey(CityDict, verbose_name=u"city", on_delete=models.CASCADE)
    students = models.IntegerField(default=0, verbose_name=u"people learn")
    course_nums = models.IntegerField(default=0, verbose_name=u"course number")

    class Meta:
        verbose_name = u"organization"
        verbose_name_plural = verbose_name

    # def get_teacher_nums(self):
    #     #获取课程机构的教师数量
    #     return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(BaseModel):
    org = models.ForeignKey(CourseOrg, verbose_name=u"organization", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u"teacher name")
    work_years = models.IntegerField(default=0, verbose_name=u"working year")
    work_company = models.CharField(max_length=50, verbose_name=u"organization name")
    work_position = models.CharField(max_length=50, verbose_name=u"title in company")
    points = models.CharField(max_length=50, verbose_name=u"teaching characteristic")
    click_nums = models.IntegerField(default=0, verbose_name=u"click")
    fav_nums = models.IntegerField(default=0, verbose_name=u"favor")
    age = models.IntegerField(default=18, verbose_name=u"age")
    image = models.ImageField(default='', upload_to="teacher/%Y/%m",
                              verbose_name=u"profile image", max_length=100)

    class Meta:
        verbose_name = u"teacher"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # def get_course_nums(self):
    #     return self.course_set.all().count()