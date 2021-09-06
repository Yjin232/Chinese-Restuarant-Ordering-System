# python
#-*- coding:utf-8 -*-
# @Time    : 2021/8/18 20:14
# @Author  : Kamisangma
#自定义中间件类，执行是否登录判断
from django.shortcuts import redirect
from django.urls import reverse
import re

class ShopMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print('ShopMiddleware')
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        #后台拦截操作
        path = request.path
        #判断管理后台是否登录,
        #定义不登录也可以直接访问的url列表
        urllist = ['/myadmin/login','/myadmin/dologin','/myadmin/logout','/myadmin/verify']
        # 若未登录则重定向去登录界面,并且不再urllist中，才做登陆判断
        if re.match(r'^/myadmin',path) and path not in urllist:
            #使用session判断是否操作(若在session中没有adminuser)
            if 'adminuser' not in request.session:
                #重定向去登录页面
                return redirect(reverse("myadmin_login"))
                # pass
        #若已经登录，则正常通过该中间件

        # 前台拦截操作
        # 判断大堂点餐请求是否登录，(session 是否有 webuser标志)
        # 若未登录则重定向去登录界面,并且不再urllist中，才做登陆判断
        if re.match(r'^/web', path):
        # 使用session判断是否操作(若在session中没有webuser)
            if 'webuser' not in request.session:
                # 重定向去大堂点餐登录页面
                return redirect(reverse("web_login"))

        # 若已经登录，则正常通过该中间件

        # 移动端拦截操作
        # 判断移动端点餐请求是否登录，(session 是否有 mobileuser标志)
        # 若未登录则重定向去登录界面,并且不再urllist中，才做登陆判断
        # 定义不登录也可以直接访问的url列表
        urllist = ['/mobile/register', '/mobile/doregister']
        if re.match(r'^/mobile', path) and (path not in urllist):
            # 使用session判断是否操作(若在session中没有,mobileuser)
            if 'mobileuser' not in request.session:
                # 重定向去大堂点餐登录页面
                return redirect(reverse("mobile_register"))

        # 若已经登录，则正常通过该中间件




        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response