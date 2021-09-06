# python
#-*- coding:utf-8 -*-
# @Time    : 2021/8/18 12:50
# @Author  : Kamisangma

#店铺信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Shop
from django.core.paginator import Paginator
from datetime import datetime
import random
import time

def index(request,pindex=1):
    """游览店铺信息"""
    smod = Shop.objects
    slist = smod.filter(status__lt=9) #状态为9的信息已经被删除，不用展示在界面中
    mywhere = [] #保存搜索条件状态
    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)
    if kw:
        slist = slist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        slist = slist.filter(status=status)
        mywhere.append("status=" + status)

    slist = slist.order_by('id') #对shop数据以id号进行排序
    #执行分页
    pindex = int(pindex)
    p = Paginator(slist,3) #每页五条数据
    maxpages = p.num_pages #获取最大页数
    #防止页数溢出
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    list2 = p.page(pindex)#获取当前页数据
    plist = p.page_range#获取页码列表信息

    context = {'shoplist':list2,'plist':plist,'pindex':pindex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/shop/index.html',context)


def add(request):
    """加载添加店铺信息表单"""
    return render(request,'myadmin/shop/add.html')


def insert(request):
    """执行插入信息"""
    try:
        #店铺封面图片的上传处理,详见django框架
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            return HttpResponse('Cover_pic Requires!')
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + cover_pic, 'wb+')
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()

        #店铺logo的上传处理
        myfile = request.FILES.get("banner_pic", None)
        if not myfile:
            return HttpResponse('Banner_pic Requires!')
        banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/shop/" + banner_pic, 'wb+')
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()

        #实例化model，分装信息，并执行添加操作
        ob= Shop()
        ob.name = request.POST['name']
        ob.address = request.POST['address']
        ob.phone = request.POST['phone']
        ob.banner_pic = banner_pic
        ob.cover_pic = cover_pic
        ob.status = 1

        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': 'Add Success!'}
    except:
        context = {'info': 'Sorry! Please check your FORM!'}

    return render(request,'myadmin/info.html',context)


def delete(request,sid=0):
    """删除信息"""
    try:
        ob = Shop.objects.get(id = sid)
        ob.status = 9 #将状态改为9，不显示在用户信息界面
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #将修改时间改成当前时间
        ob.save() #执行保存
        context = {'info': 'Delete Success!'}
    except:
        context = {'info': 'Failure! Please check the Id!'}

    return render(request, 'myadmin/info.html', context)


def edit(request,sid=0):
    """加载修改信息表单"""
    try:
        ob = Shop.objects.get(id=sid)
        context = {'shop': ob}
        return render(request,'myadmin/shop/edit.html',context)
    except:
        context = {'info': 'Failure! Please check the shop Id!'}

        return render(request, 'myadmin/info.html', context)


def update(request,sid=0):
    """修改信息"""
    try:
        ob = Shop.objects.get(id=sid)
        ob.name = request.POST['name']
        ob.status = request.POST['status']
        ob.address = request.POST['address']
        ob.phone = request.POST['phone']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 将修改时间改成当前时间
        ob.save()  # 执行保存
        context = {'info': 'Update Success!'}
    except:
        context = {'info': 'Failure!'}

    return render(request, 'myadmin/info.html', context)

