"""stutea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.shortcuts import render
from django.views import View
from .view import *
from .grade import *
from .stage import *
from .types import *
from .shiti import *
from .zuti import *
urlpatterns = [
    path('admin/', admin.site.urls),
    # 进入主界面
    path("",studentIndex),
    # 登陆
    path("login/",login),
    #退出
    path("out/",out),
    # 注册
    path("reg/",reg),
    # 登陆进入的主页
    path("studentInfo/",studentInfo),
    #添加学生信息
    path("add/",add),
    path("dele/",dele),
    path("edit/",edit),
    path("search/",search),

    # 教师信息
    path("teacherInfo/",teacherInfo),
    path("teadele/",teadele),
    path("teasearch/",teasearch),
    path("teacheradd/",teacheradd),
    path("teacheredit/",teacheredit),
    # 班级信息
    path("classInfo/",classInfo),
    path("classadd/",classadd),
    path("classdele/",classdele),
    path("classsearch/",classsearch),
    path("classedit/",classedit),

    #双击查询
    path("addCon/",addCon),
    # 异步验证
    path("ajax/",ajax),
    path("sajax/",sajax),

    # 年级表
    path("grade/",grade.as_view()),
    path("gradeadd/",gradeadd.as_view()),
    path("gradedit/",gradedit.as_view()),
    path("gradedele/",gradedele.as_view()),
    path("gradetype/",gradetype.as_view()),
    # 学科表
    path("stage/",stage.as_view()),
    path("stageadd/",stageadd.as_view()),
    path("stagedel/",stagedel.as_view()),
    path("stagedit/",stagedit.as_view()),
    path("stagetype/",stagetype.as_view()),
    #题型
    path("types/",types.as_view()),
    path("typesadd/",typesadd.as_view()),
    path("shiti/",shiti.as_view()),
    path("shitiadd/",shitiadd.as_view()),
    path("typeshiti/",typeshiti.as_view()),
    path("fileload/",fileload.as_view()),
    path("shitisearch/",shitisearch.as_view()),
    # 组题
    path("zuti/",zuti.as_view()),
    path("zutiadd/",zutiadd.as_view()),
    path("zutisearch/",zutisearch.as_view()),
    #临时表
]
