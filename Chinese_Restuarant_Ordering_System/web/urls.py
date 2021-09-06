# python
#-*- coding:utf-8 -*-
# @Time    : 2021/8/18 10:43
# @Author  : Kamisangma

#当前为web端子路由
from django.urls import path, include
from .views import index, cart, orders


urlpatterns = [
    path('', index.index,name='web_index'),#访问前端的index页

    #前台登录退出路由配置
    path('login', index.login,name='web_login'),
    path('dologin', index.dologin,name='web_dologin'),
    path('logout', index.logout,name='web_logout'),
    path('verify', index.verify,name='web_verify'),

    #为访问点菜大堂界面的url路由请求自动添加web前缀的路由
    path('web/', include([
        path('', index.webindex,name='web_index'),
        # 购物车信息管理路由配置
        path('cart/add/<str:pid>', cart.add, name="web_cart_add"), #购物车添加
        path('cart/del/<str:pid>', cart.delete, name="web_cart_del"),#购物车删除
        path('cart/clear', cart.clear, name="web_cart_clear"), #购物车清空
        path('cart/change', cart.change, name="web_cart_change"),#购物车更改

        #订单管理信息路由配置
        path('orders/<int:pindex>', orders.index, name="web_orders_index"),  # 执行订单添加
        path('orders/insert', orders.insert, name="web_orders_insert"),  # 执行订单添加
        path('orders/detail', orders.detail,name='web_orders_detail'), #订单的详情信息
        path('orders/status', orders.status,name='web_orders_status'), #修改订单状态

    ]) )
]