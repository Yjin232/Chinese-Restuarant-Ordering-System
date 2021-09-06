# python
#-*- coding:utf-8 -*-
# @Time    : 2021/8/18 10:42
# @Author  : Kamisangma


#当前为移动端子路由
from django.urls import path
from .views import index, member, cart

urlpatterns = [
    path('', index.index,name='mobile_index'),#访问移动端的index页
    #会员注册或者登录
    path('register', index.register,name='mobile_register'),#访问移动端的会员登录页
    path('doregister', index.doregister,name='mobile_doregister'),#执行会员登录
    #店铺选择
    path('shop', index.shop,name='mobile_shop'),#访问移动端的shop选择页面
    path('shop/select', index.selectshop,name='mobile_selectshop'),#执行shop选择
    #订单处理
    path('orders/add', index.addorders,name='mobile_addorders'),#添加订单
    path('orders/doadd', index.doaddorders, name='mobile_doaddorders'),  # 执行移动端添加订单

    #会员中心
    path('member', member.index,name='mobile_member_index'),#访问移动端的会员中心index页
    path('member/orders', member.orders,name='mobile_member_orders'),#访问会员中心我的订单页面
    path('member/detail', member.detail,name='mobile_member_detail'),#订单详情页面
    path('member/logout', member.logout,name='mobile_member_logout'),#执行退出
    #购物车路由
    path('cart/add', cart.add, name='mobile_cart_add'),  # 购物车添加
    path('cart/delete', cart.delete, name='mobile_cart_delete'),  # 购物车删除
    path('cart/clear', cart.clear, name='mobile_cart_clear'),  # 购物车清空
    path('cart/change', cart.change, name='mobile_cart_change'),  # 改变购物车

]