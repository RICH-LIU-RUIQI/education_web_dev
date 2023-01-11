import django.db.models
from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher, CourseOrg
# Create your models here.

# 1.设计表结构有几个重要的点
# 实体1 <关系> 实体2
# 课程
# <一对多>章节 <一对多>视频 <一对一>课程资源(所以这个直接加在课程表里面)
# 2. 实体的具体字段
# 3. 每个字段的类型，是否必填


class Course(BaseModel):
    # less join > more fileds
    course_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Lecturer', default='')
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, default='')
    name = models.CharField(verbose_name='course name', max_length=64)

    descr = models.CharField(verbose_name='course description', max_length=400)
    learn_times = models.IntegerField(default=0, verbose_name='courses time min')
    degree = models.CharField(verbose_name='course level', choices=(
        ('e', 'easy'),
        ('m', 'medium'),
        ('h', 'hard')
    ), max_length=1)
    students = models.IntegerField(default=0, verbose_name='student number')
    fav_num = models.IntegerField(default=0, verbose_name='favorite number')
    click_num = models.IntegerField(default=0, verbose_name='click times')
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"course pict", max_length=100)
    notice = models.CharField(verbose_name='course statement', max_length=100, default='')
    category = models.CharField(default='backend', max_length=20, verbose_name=u"courses category")
    tag = models.CharField(default="", verbose_name=u"course tag", max_length=10)
    youneed_know = models.CharField(default="", max_length=300, verbose_name="must know about course")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="advice")
    detail = models.TextField(verbose_name=u"course detail",default='')
    if_classical = models.BooleanField(default=False, verbose_name='if classical')

    class Meta:
        verbose_name = 'course information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name  # display course name

    def get_lesson_num(self):
        # obtain outer keys data
        return self.lesson_set.all().count()

    def get_all_tags(self):
        # get all tags
        all_tags = self.coursetag_set.all()
        return [tag.tag for tag in all_tags]


class Lesson(BaseModel):
    parent_course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='lesson name')
    learn_time = models.IntegerField(default=0, verbose_name='learning time')

    class Meta:
        verbose_name = 'course lessons'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    parent_lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='lesson name')
    learn_time = models.IntegerField(default=0, verbose_name='learning time')
    url = models.CharField(max_length=200, verbose_name='visit url')

    class Meta:
        verbose_name = 'lesson video'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    parent_course = models.ForeignKey(to=Course, verbose_name="course", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="name")
    download = models.FileField(upload_to="course/resource/%Y/%m",
                                verbose_name="source file", max_length=100)

    class Meta:
        verbose_name = "course material"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseTag(BaseModel):
    # one(course) vs multi(tags)
    tar_course = models.ForeignKey(to=Course, on_delete=models.CASCADE, verbose_name='lecture')
    tag = models.CharField(max_length=100, verbose_name='tag')

    class Meta:
        verbose_name = 'course vs tag'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag




