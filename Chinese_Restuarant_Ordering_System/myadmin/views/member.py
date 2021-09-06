# python
#-*- coding:utf-8 -*-
# @Time    : 2021/8/20 17:40
# @Author  : Kamisangma
#会员信息视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

from myadmin.models import Member

# ==============后台会员信息管理======================
# 浏览会员信息
def index(request,pindex=1):
    mod = Member.objects
    list = mod.filter(status__lt=9)
    mywhere = []  # 保存搜索条件状态
    # 获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    if kw:
        list = list.filter(nickname__contains=kw)
        mywhere.append('keyword=' + kw)

    #执行分页处理
    pindex = int(pindex)
    page = Paginator(list,5) #以5条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    list2 = page.page(pindex) #当前页数据
    plist = page.page_range   #页码数列表

    #封装信息加载模板输出
    context = {"memberlist":list2,'plist':plist,'pindex':pindex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/member/index.html",context)

# def resetpassword(request,mid=0):
#     try:
#         ob = Member.objects.get(id = mid)
#         ob.