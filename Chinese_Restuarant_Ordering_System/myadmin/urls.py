# python
#-*- coding:utf-8 -*-
# @Time    : 2021/8/18 10:43
# @Author  : Kamisangma

#后台管理子路由
from django.urls import path
from .views import index
from .views import user
from .views import shop
from .views import category
from .views import product
from .views import member
from .views import orders

urlpatterns = [
    path('', index.index,name='myadmin_index'),#访问后台管理的index页

    #后台管理员登录，退出路由
    path('login', index.login,name='myadmin_login'), #加载登录表单
    path('dologin', index.dologin,name='myadmin_dologin'), #执行登录路由
    path('logout', index.logout,name='myadmin_logout'),#执行退出路由
    path('verify', index.verify,name='myadmin_verify'),#输出验证码

    #店铺信息管理路由
    path('shop/<int:pindex>', shop.index, name='myadmin_shop_index'),  # 游览
    path('shop/add', shop.add, name='myadmin_shop_add'),  # 添加表单
    path('shop/insert', shop.insert, name='myadmin_shop_insert'),  # 执行添加
    path('shop/delete/<int:sid>', shop.delete, name='myadmin_shop_delete'),  # 执行删除
    path('shop/edit/<int:sid>', shop.edit, name='myadmin_shop_edit'),  # 编辑表单
    path('shop/update/<int:sid>', shop.update, name='myadmin_shop_update'),  # 执行编辑

    #员工信息管理路由
    path('user/<int:pindex>', user.index, name='myadmin_user_index'),  # 游览
    path('user/add', user.add, name='myadmin_user_add'),  # 添加表单
    path('user/insert', user.insert, name='myadmin_user_insert'),  # 执行添加
    path('user/delete/<int:uid>', user.delete, name='myadmin_user_delete'),  # 执行删除
    path('user/edit/<int:uid>', user.edit, name='myadmin_user_edit'),  # 编辑表单
    path('user/update/<int:uid>', user.update, name='myadmin_user_update'),  # 执行编辑

    #菜品分类管理路由
    path('category/<int:pindex>', category.index, name='myadmin_category_index'),  # 游览
    path('category/load/<int:sid>', category.loadCategory, name="myadmin_category_load"), #加载菜品表单
    path('category/add', category.add, name='myadmin_category_add'),  # 添加表单
    path('category/insert', category.insert, name='myadmin_category_insert'),  # 执行添加
    path('category/delete/<int:cid>', category.delete, name='myadmin_category_delete'),  # 执行删除
    path('category/edit/<int:cid>', category.edit, name='myadmin_category_edit'),  # 编辑表单
    path('category/update/<int:cid>', category.update, name='myadmin_category_update'),  # 执行编辑

    #菜品信息管理路由
    path('product/<int:pindex>', product.index, name='myadmin_product_index'),  # 游览
    path('product/add', product.add, name='myadmin_product_add'),  # 添加表单
    path('product/insert', product.insert, name='myadmin_product_insert'),  # 执行添加
    path('product/delete/<int:fid>', product.delete, name='myadmin_product_delete'),  # 执行删除
    path('product/edit/<int:fid>', product.edit, name='myadmin_product_edit'),  # 编辑表单
    path('product/update/<int:fid>', product.update, name='myadmin_product_update'),  # 执行编辑

    # 会员管理路由
    path('member/<int:pindex>', member.index, name="myadmin_member_index"),  # 浏览会员

    # 订单路由
    path('orders/<int:pindex>', orders.index, name="myadmin_orders_index"),  # 浏览订单
]