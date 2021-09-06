# python
#-*- coding:utf-8 -*-
# @Time    : 2021/8/18 12:50
# @Author  : Kamisangma

#员工信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import random

def index(request,pindex=1):
    """游览信息"""
    umod = User.objects
    ulist = umod.filter(status__lt=9) #状态为9的信息已经被删除，不用展示在界面中
    mywhere = [] #保存搜索条件状态
    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)
    if kw:
        #多条件搜索语法 .filter(Q(query) | Q(query))
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append('keyword='+kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)

    #执行分页
    pindex = int(pindex)
    p = Paginator(ulist,5) #每页五条数据
    maxpages = p.num_pages #获取最大页数
    #防止页数溢出
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    list2 = p.page(pindex)#获取当前页数据
    plist = p.page_range#获取页码列表信息

    context = {'userlist':list2,'plist':plist,'pindex':pindex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/user/index.html',context)


def add(request):
    """加载添加信息表单"""
    return render(request,'myadmin/user/add.html')


def insert(request):
    """执行插入信息"""
    try:
        ob= User()
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        ob.status = 1

        # 将当前员工信息的密码做md5处理
        # 获取密码并md5
        import hashlib
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password'] + str(n) #从POST表单获取用户输入的密码并添加一个干扰值输入数据库
        md5.update(s.encode('utf-8')) #将要产生md5的子串放进去
        ob.password_hash = md5.hexdigest() #获取md5值
        ob.password_salt = n

        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': 'Add Success!'}
    except:
        context = {'info': 'Sorry! Please check your FORM!'}

    return render(request,'myadmin/info.html',context)


def delete(request,uid=0):
    """删除信息"""
    try:
        ob = User.objects.get(id = uid)
        ob.status = 9 #将状态改为9，不显示在用户信息界面
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #将修改时间改成当前时间
        ob.save() #执行保存
        context = {'info': 'Delete Success!'}
    except:
        context = {'info': 'Failure! Please check the Id!'}

    return render(request, 'myadmin/info.html', context)


def edit(request,uid=0):
    """加载修改信息表单"""
    try:
        ob = User.objects.get(id=uid)
        context = {'user': ob}
        return render(request,'myadmin/user/edit.html',context)
    except:
        context = {'info': 'Failure! Please check the Id!'}

        return render(request, 'myadmin/info.html', context)


def update(request,uid=0):
    """修改信息"""
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST['nickname']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 将修改时间改成当前时间
        ob.save()  # 执行保存
        context = {'info': 'Update Success!'}
    except:
        context = {'info': 'Failure!'}

    return render(request, 'myadmin/info.html', context)

