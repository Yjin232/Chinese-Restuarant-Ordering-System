# python
#-*- coding: utf-8 -*-
# @Time    : 2021/8/20 10:35
# @Author  : Kamisangma
# python
#-*- coding:utf-8 -*-
# @Time    : 2021/8/18 12:50
# @Author  : Kamisangma

#菜品信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from myadmin.models import Product, Category, Shop
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import random
import time, os

def index(request,pindex=1):
    """游览信息"""
    fmod = Product.objects
    flist = fmod.filter(status__lt=9) #状态为9的信息已经被删除，不用展示在界面中
    mywhere = [] #保存搜索条件状态
    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)
    if kw:
        flist = flist.filter(name__contains=kw)
        mywhere.append('keyword='+kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        flist = flist.filter(status=status)
        mywhere.append("status=" + status)

    # 获取、判断并封装菜品类别category_id搜索条件
    cid = request.GET.get('category_id', '')
    if cid != '':
        flist = flist.filter(category_id=cid)
        mywhere.append("category_id=" + cid)


    #执行分页
    pindex = int(pindex)
    p = Paginator(flist,6) #每页五条数据
    maxpages = p.num_pages #获取最大页数
    #防止页数溢出
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    list2 = p.page(pindex)#获取当前页数据
    plist = p.page_range#获取页码列表信息

    # 遍历信息，并获取对应的商铺名称，以shopname名封装
    for vo in list2:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name #追加数据进list2

    # 遍历信息，并获取对应的菜品分类名称，以categoryname名封装
    for vo in list2:
        sob = Category.objects.get(id=vo.category_id)
        vo.categoryname = sob.name  # 追加数据进list2

    context = {'productlist':list2, 'plist':plist,'pindex':pindex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/product/index.html',context)


def add(request):
    """加载添加信息表单"""
    slist = Shop.objects.values("id", "name")
    clist = Category.objects.values("id", "name")
    context = {"shoplist": slist,"categorylist":clist}
    return render(request, "myadmin/product/add.html", context)



def insert(request):
    """执行插入信息"""

    try:
        #店铺封面图片的上传处理,详见django框架
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return HttpResponse('Cover_pic Requires!')
        cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        destination = open("./static/uploads/product/" + cover_pic, 'wb+')
        for chunk in myfile.chunks():
            destination.write(chunk)
        destination.close()

        ob = Product()
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.cover_pic = cover_pic
        ob.save()
        context = {'info': 'Add Success!'}
    except:
        context = {'info': 'Sorry! Please check your FORM!'}

    return render(request,'myadmin/info.html', context)


def delete(request,fid=0):
    """删除信息"""
    try:
        ob = Product.objects.get(id = fid)
        ob.status = 9 #将状态改为9，不显示在用户信息界面
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #将修改时间改成当前时间
        ob.save() #执行保存
        context = {'info': 'Delete Success!'}
    except:
        context = {'info': 'Failure! Please check the Id!'}

    return render(request, 'myadmin/info.html', context)


def edit(request,fid):
    '''加载编辑信息页面'''
    try:
        ob = Product.objects.get(id=fid)
        slist = Shop.objects.values("id","name")
        clist = Category.objects.values("id", "name")
        context={"product":ob,"shoplist":slist,'categorylist':clist}
        return render(request,"myadmin/product/edit.html",context)
    except:
        context={"info":"Failure! Please check the Id!"}
        return render(request,"myadmin/info.html",context)


def update(request,fid=0):
    """修改信息"""
    try:
        #修改图片的操作
        # 获取原图片名
        oldpicname = request.POST['oldpicname']
        # 判断是否有文件上传
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            cover_pic = oldpicname
        else:
            # 图片的上传处理
            cover_pic = str(time.time()) + "." + myfile.name.split('.').pop()
            destination = open("./static/uploads/product/" + cover_pic, "wb+")
            for chunk in myfile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

        ob = Product.objects.get(id=fid)
        ob.name = request.POST['name']
        ob.category_id = request.POST['category_id']
        ob.shop_id = request.POST['shop_id']
        ob.price = request.POST['price']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 将修改时间改成当前时间
        ob.cover_pic = cover_pic
        ob.save()  # 执行保存
        context = {'info': 'Update Success!'}

        #若有新图片，则删除老图片
        if myfile:
            os.remove('./static/uploads/product/' + oldpicname)

    except:
        context = {'info': 'Failure!'}
        # 若有新图片，则删除老图片
        if myfile:
            os.remove('./static/uploads/product/' + cover_pic)

    return render(request, 'myadmin/info.html', context)

