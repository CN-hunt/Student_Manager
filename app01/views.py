from django import forms
from django.db.models import Count
from django.shortcuts import render, redirect, HttpResponse
from pandas.core.indexers import objects
from app01 import models
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe

from app01.models import teachers
from django.utils.translation import gettext_lazy as _


# Create your views here.


class teacherModelForm(forms.ModelForm):
    class Meta:
        model = models.teachers
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),

        }

    # 去重以及规定号码格式
    # 重点在于 clean_ 要处理哪个字段后面就是那个字段的名称,后面同理
    def clean_number(self):
        number = self.cleaned_data['number']
        exists = models.teachers.objects.filter(number=number).exists()  # 判断数据（电话号码）是否唯一，赋予的结果是一个布尔类型的值
        if len(number) != 11:
            raise ValidationError(_('格式错误'))
        elif exists:
            raise ValidationError(_('号码已经存在'))
        return number

    def clean_name(self):
        name = self.cleaned_data['name']
        exists = models.teachers.objects.filter(name=name).exists()
        if len(name) <= 1:
            raise ValidationError(_('格式错误'))
        elif exists:
            raise ValidationError(_('班主任已存在'))
        return name


def teacher_add(request):
    """教师表及已添加教师展示"""

    form = teacherModelForm()
    data = models.teachers.objects.all()
    if request.method == 'GET':
        return render(request, 'teachers_add.html', {'form': form, 'data': data})
    form = teacherModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return render(request, 'teachers_add.html', {'form': form, 'data': data})
    return render(request, 'teachers_add.html', {'form': form, 'data': data})


def teacher_del(request, nid):
    """删除教师"""
    if request.method == 'GET':
        models.teachers.objects.get(id=nid).delete()
        return redirect('/index/teacheradd/')


# 以下为学生相关的界面
class studentModelForm(forms.ModelForm):
    class Meta:
        model = models.students
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }

    # def clean_number(self):
    #     number = self.cleaned_data['number']
    #     exists = models.students.objects.filter(number=number).exists()
    #     if len(number) != 8:
    #         raise ValidationError('格式错误')
    #     elif exists:
    #         raise ValidationError('学号已经存在')
    #     return number

    def clean_number(self):
        number = self.cleaned_data['number']
        if len(number) != 8:
            raise ValidationError(_('格式错误'))

        # 检查是否是创建新记录还是更新现有记录
        if self.instance and self.instance.pk:  # 这是更新操作
            exists = models.students.objects.filter(number=number).exclude(pk=self.instance.pk).exists()
        else:  # 这是创建操作
            exists = models.students.objects.filter(number=number).exists()

        if exists:
            raise ValidationError(_('学号已经存在'))

        return number


def student_list(request):
    """学生列表界面"""
    if request.method == 'GET':
        students = models.students.objects.all()
        return render(request, 'student_list.html', {'students': students})


def student_add(request):
    """学生添加界面"""

    form = studentModelForm()
    # students = models.students.objects.all()
    if request.method == 'POST':
        form = studentModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/index/studentcontent/')
        return render(request, 'student_add.html', {'form': form, })


def student_del(request, nid):
    # 删除学生
    if request.method == "GET":
        models.students.objects.get(id=nid).delete()
        return redirect('/index/studentcontent/')


def student_edit(request, nid):
    """编辑学生"""
    if request.method == 'GET':
        edit = models.students.objects.filter(id=nid).first()
        form = studentModelForm(instance=edit)
        return render(request, 'student_edit.html', {'form': form, })
    edit = models.students.objects.filter(id=nid).first()
    form = studentModelForm(data=request.POST, instance=edit)
    if form.is_valid():
        form.save()
        return redirect('/index/studentcontent/')
    return render(request, 'student_edit.html', {'form': form})


def index(request):
    """主页"""
    students = models.students.objects.all()

    # 获取所有班主任及其学生人数统计
    # 使用annotate添加student_count字段
    teacher_data = teachers.objects.annotate(
        student_count=Count('students')
    ).order_by('-student_count')  # 按学生数量降序排列
    # 计算学生总数
    # total_students = students.objects.count()
    # 找出最大班级人数作为参考基准
    max_count = max([t.student_count for t in teacher_data]) if teacher_data else 1
    return render(request, 'index.html', {'students': students, 'teacher_data': teacher_data, 'max_count': max_count})


def student_content(request):
    """学生信息展示及添加"""
    students = models.students.objects.all()

    form = studentModelForm()

    search_dict = {}
    search = request.GET.get('Q')  # 获取搜索框的结果
    if search:
        search_dict['number__contains'] = search
    search_content = models.students.objects.filter(**search_dict)
    paginator = Paginator(search_content, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'student_content.html', {'page_obj': page_obj, 'students': students, 'form': form})


# 以下为登录设置
class AdminModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-text form-control'}),  # 这样就可以给这个输入框设置两个前端样式
            'password': forms.PasswordInput(attrs={'class': 'form-text form-control'}),
        }



def login(request):
    """登录界面"""
    form = AdminModelForm()
    if request.method == 'GET':
        return render(request, 'login.html', {'form': form})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        print(admin_obj)
        if not admin_obj:
            errors = '<span style="color: red">用户名或密码错误</span>'
            errors = mark_safe(errors)
            return render(request, 'login.html', {'form': form, 'errors': errors})
        request.session['info'] = {'id': admin_obj.id, 'username': admin_obj.username}
        return redirect('/index/')


def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/index/login/')


def admin_manager(request):
    """管理员展示及添加"""
    content_form = AdminModelForm()
    form = models.Admin.objects.all()
    return render(request, 'admin_manager.html', {'form': form, 'content_form': content_form})


def admin_del(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/index/admin_manager/')


# 管理员信息填写出错时跳转
def admin_add_error(request):
    if request.method == "GET":
        return render(request, 'admin_error.html', {'form': AdminModelForm()})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/index/admin_manager/')
    return render(request, 'admin_error.html', {'form': form})


def admin_add(request):
    form = AdminModelForm()
    if request.method == 'POST':
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/index/admin_manager/')
        return redirect('/index/admin_error/')
