# python
#-*- coding:utf-8 -*-
# @Time    : 2021/8/18 12:50
# @Author  : Kamisangma

#菜品类别管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from myadmin.models import Category, Shop
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import random

def index(request,pindex=1):
    """游览信息"""
    cmod = Category.objects
    clist = cmod.filter(status__lt=9) #状态为9的信息已经被删除，不用展示在界面中
    mywhere = [] #保存搜索条件状态
    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)
    if kw:
        clist = clist.filter(name=kw)
        mywhere.append('keyword='+kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        clist = clist.filter(status=status)
        mywhere.append("status=" + status)

    #执行分页
    pindex = int(pindex)
    p = Paginator(clist,10) #每页五条数据
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

    context = {'categorylist':list2,'plist':plist,'pindex':pindex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/category/index.html',context)


def loadCategory(request,sid):
    clist = Category.objects.filter(status__lt=9,shop_id=sid).values("id","name")
    #返回QuerySet对象，使用list强转成对应的菜品分类列表信息
    return JsonResponse({'data':list(clist)})


def add(request):
    """加载添加信息表单"""
    slist = Shop.objects.values("id", "name")
    context = {"shoplist": slist}
    return render(request, "myadmin/category/add.html", context)



def insert(request):
    """执行插入信息"""
    try:
        ob = Category()
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': 'Add Success!'}
    except:
        context = {'info': 'Sorry! Please check your FORM!'}

    return render(request,'myadmin/info.html',context)


def delete(request,cid=0):
    """删除信息"""
    try:
        ob = Category.objects.get(id = cid)
        ob.status = 9 #将状态改为9，不显示在用户信息界面
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #将修改时间改成当前时间
        ob.save() #执行保存
        context = {'info': 'Delete Success!'}
    except:
        context = {'info': 'Failure! Please check the Id!'}

    return render(request, 'myadmin/info.html', context)


def edit(request,cid):
    '''加载编辑信息页面'''
    try:
        ob = Category.objects.get(id=cid)
        slist = Shop.objects.values("id","name")
        context={"category":ob,"shoplist":slist}
        return render(request,"myadmin/category/edit.html",context)
    except:
        context={"info":"Failure! Please check the Id!"}
        return render(request,"myadmin/info.html",context)


def update(request,cid=0):
    """修改信息"""
    try:
        ob = Category.objects.get(id=cid)
        ob.name = request.POST['name']
        ob.shop_id = request.POST['shop_id']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 将修改时间改成当前时间
        ob.save()  # 执行保存
        context = {'info': 'Update Success!'}
    except:
        context = {'info': 'Failure!'}

    return render(request, 'myadmin/info.html', context)

