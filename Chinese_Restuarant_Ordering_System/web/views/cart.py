# python
#-*- coding:utf-8 -*-
# @Time    : 2021/8/21 21:06
# @Author  : Kamisangma
#购物车信息管理视图文件
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

def add(request, pid):
    """添加购物车"""
    #从session中的菜品列表productlist中获取要添加购物车中的菜品信息
    # 这里需要返回一个pid（product_id），也就是在index界面中点击加入购物车按钮后会调用
    # add方法
    product = request.session['productlist'][pid]
    product['num'] = 1 #为product实例追加一个数量数据，默认为1
    #从session中获取购物车cartlist信息，若没有的话默认为空字典
    cartlist = request.session.get('cartlist',{})
    #判断购物车中是否已经存在要加入购物车的商品
    if pid in cartlist:
        cartlist[pid]['num'] += product['num']
    else:
        cartlist[pid] = product #将菜品所有信息 放入购物车
    #将购物车中的商品信息放回到session中
    request.session['cartlist'] = cartlist
    #跳转到点餐首页
    return redirect(reverse('web_index'))

def delete(request, pid):
    """删除购物车中的商品"""
    cartlist = request.session['cartlist']
    del cartlist[pid]
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))

def clear(request):
    """清空购物车"""
    request.session['cartlist'] = {}
    return redirect(reverse('web_index'))

def change(request):
    """购物车信息修改"""
    cartlist = request.session['cartlist']
    shopid = request.GET.get("pid", 0)
    num = int(request.GET.get('num', 1))
    if num < 1:
        num = 1
    cartlist[shopid]['num'] = num
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))