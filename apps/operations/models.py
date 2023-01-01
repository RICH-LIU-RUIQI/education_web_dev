from django.db import models
from django.contrib.auth import get_user_model

from apps.users.models import BaseModel
from apps.courses.models import Course

# Create your models here.
UserProfile = get_user_model()  # get from setting


class UserAsk(BaseModel):
    name = models.CharField(max_length=20, verbose_name="name")
    mobile = models.CharField(max_length=11, verbose_name="phone number")
    course_name = models.CharField(max_length=50, verbose_name="course title")

    class Meta:
        verbose_name = "user request"
        verbose_name_plural = verbose_name


class CourseComments(BaseModel):
    user = models.ForeignKey(UserProfile, verbose_name="user", on_delete=models.CASCADE)
    parent_course = models.ForeignKey(Course, verbose_name="course", on_delete=models.CASCADE)
    comments = models.CharField(max_length=200, verbose_name="comment")

    class Meta:
        verbose_name = "Course Comment"
        verbose_name_plural = verbose_name


class UserFavorite(BaseModel):

    user = models.ForeignKey(UserProfile, verbose_name="user", on_delete=models.CASCADE)
    fav_id = models.IntegerField(default=0, verbose_name="id")
    fav_type = models.IntegerField(choices=(
        (1,"course name"),(2,"course organization"),(3,"lecturer")),
        default=1, verbose_name="favorite type")

    class Meta:
        verbose_name = "favorite"
        verbose_name_plural = verbose_name


class UserMessage(BaseModel):
    user = models.IntegerField(default=0, verbose_name="user")
    message = models.CharField(max_length=500, verbose_name="content")
    has_read = models.BooleanField(default=False, verbose_name="if read")

    class Meta:
        verbose_name = "user information"
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="user", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="courses", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "users' courses"
        verbose_name_plural = verbose_name
