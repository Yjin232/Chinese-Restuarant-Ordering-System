# python
#-*- coding: utf-8 -*-
# @Time    : 2021/8/20 10:35
# @Author  : Kamisangma
# python
#-*- coding:utf-8 -*-
# @Time    : 2021/8/18 12:50
# @Author  : Kamisangma

#订单信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from myadmin.models import Member, User, Shop, Orders
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
import random
import time, os

def index(request,pindex=1):
    """游览信息"""
    omod = Orders.objects
    olist = omod.filter(status__lt=10) #状态为9的信息已经被删除，不用展示在界面中
    mywhere = [] #保存搜索条件状态
    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)
    if kw:
        olist = olist.filter(money__gte=kw)
        mywhere.append('keyword='+kw)
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        olist = olist.filter(status=status)
        mywhere.append("status=" + status)

    # 获取、判断并封装菜品类别shop_id搜索条件
    sid = request.GET.get('shop_id', '')
    if sid != '':
        olist = olist.filter(shop_id=sid)
        mywhere.append("category_id=" + sid)


    #执行分页
    pindex = int(pindex)
    p = Paginator(olist,6) #每页五条数据
    maxpages = p.num_pages #获取最大页数
    #防止页数溢出
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    list2 = p.page(pindex)#获取当前页数据
    plist = p.page_range#获取页码列表信息

    # 遍历信息，并获取对应的商铺,会员，管理员名称，以shopname,username,membername名封装
    for vo in list2:
        sob1 = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob1.name  # 追加数据进list2
        if vo.user_id == 0:
            vo.nickname = "Mobile User"
        else:
            sob2 = User.objects.get(id=vo.user_id)
            vo.username = sob2.nickname
        if vo.member_id == 0:
            vo.membername = "The lobby order"
        else:
            sob3 = Member.objects.get(id=vo.member_id)
            vo.membername = sob3.nickname





    context = {'orderslist':list2, 'plist':plist,'pindex':pindex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,'myadmin/orders/index.html',context)


