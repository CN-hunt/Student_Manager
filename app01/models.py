from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class teachers(models.Model):
    """教师表"""
    name = models.CharField(verbose_name=_('班主任姓名'), max_length=50)
    age = models.IntegerField(verbose_name=_('年龄'), default=40)
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.IntegerField(verbose_name=_('性别'), choices=gender_choices)
    number = models.CharField(verbose_name=_('号码'), max_length=50, default=0)

    def __str__(self):
        return self.name


class students(models.Model):
    """学生表"""
    name = models.CharField(verbose_name=_('学生姓名'), max_length=50)
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.IntegerField(verbose_name=_('性别'), choices=gender_choices, default=1)
    number = models.CharField(verbose_name=_('学号'), max_length=50, )
    teacher = models.ForeignKey(verbose_name=_('班主任'), to=teachers, on_delete=models.CASCADE)


class Admin(models.Model):
    username = models.CharField(verbose_name=_('管理员姓名'), max_length=50)
    password = models.CharField(verbose_name=_('密码'), max_length=50)
