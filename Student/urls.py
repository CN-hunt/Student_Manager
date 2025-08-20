"""
URL configuration for Student project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.i18n import set_language
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('index/teacheradd/', views.teacher_add),
    path('index/<int:nid>/teacherdel/', views.teacher_del),

    # 下为学生表
    # 学生展示列表(未分页，总表)
    path('index/studentlist/', views.student_list),
    # 学生添加,已合并至studentcontent
    path('index/studentadd/', views.student_add),
    # 学生删除
    path('index/<int:nid>/studentdel/', views.student_del),
    # 学生修改
    path('index/<int:nid>/studentedit/', views.student_edit),
    # 学生列表展示及添加
    path('index/studentcontent/', views.student_content),


    # 以下为登录和管理员界面
    # 登录界面
    path('index/login/', views.login),
    # 管理员操作界面
    path('index/admin_manager/', views.admin_manager),
    # 注销
    path('index/logout/', views.logout),
    # 管理员删除
    path('index/<int:nid>/admin_del/', views.admin_del),
    # 管理员添加
    path('index/admin_add/', views.admin_add),

    path('index/admin_error/', views.admin_add_error),

    # 语言切换
    path('i18n/', include('django.conf.urls.i18n')),

]
