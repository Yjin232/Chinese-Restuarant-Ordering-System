# python
#-*- coding:utf-8 -*-
# @Time    : 2021/8/21 21:06
# @Author  : Kamisangma
#购物车信息管理视图文件
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from myadmin.models import Orders,Member,User, OrderDetail, Payment, Shop, User, Product, Category
from django.core.paginator import Paginator


def index(request,pindex=1):
    """游览信息"""
    omod = Orders.objects
    sid = request.session["shopinfo"]["id"] #获取当前店铺id号
    olist = omod.filter(shop_id=sid) #状态为9的信息已经被删除，不用展示在界面中
    mywhere = [] #保存搜索条件状态
    #获取并判断搜索条件
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        olist = olist.filter(status=status)
        mywhere.append("status=" + status)

    olist = olist.order_by("-"
                           "id")
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

    for vo in list2:
        if vo.user_id == 0:
            vo.nickname = "无"
        else:
            user = User.objects.only('nickname').get(id=vo.user_id)
            vo.nickname = user.nickname

        if vo.member_id == 0:
            vo.membername = "大堂顾客"
        else:
            member = Member.objects.only('mobile').get(id=vo.member_id)
            vo.membername = member.mobile

    context = {'orderslist':list2, 'plist':plist,'pindex':pindex,'maxpages':maxpages,'mywhere':mywhere,'url':request.build_absolute_uri()}
    return render(request,'web/list.html',context)

def insert(request):
    """执行订单添加"""
    try:
        #对orders表执行添加操作
        od = Orders()
        od.shop_id = request.session['shopinfo']['id'] #店铺id号
        od.member_id = 0
        od.user_id = request.session['webuser']['id']
        od.money = request.session['total_money']
        od.status = 1  #订单状态:1过行中/2无效/3已完成
        od.payment_status = 2  #支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        #对payment表执行添加操作
        op = Payment()
        op.order_id = od.id
        op.member_id = 0
        op.type = 2 #付款方式：1会员付款/2收银收款
        op.bank = request.GET.get("bank",3)  #收款银行渠道:1微信/2余额/3现金
        op.money = request.session['total_money']
        op.status = 2  # 订单状态:1未支付/2已支付/3已退款
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()

        # 对orderdetail表执行添加操作
        cartlist = request.session.get("cartlist",{})
        for item in cartlist.values():
            ov = OrderDetail()
            ov.order_id = od.id #订单详情中的order_id对应每个订单的id
            ov.product_id = item["id"] #菜品的id为购物车list中每个菜品的id
            ov.product_name = item["name"] #菜品的name对应catlist中每个菜品的name
            ov.price = item["price"] #单价
            ov.quantity = item["num"] #数量
            ov.status = 1 #状态：1正常；9删除
            ov.save()

        #购物完成后清空session表中的购物车和总价格信息
        del request.session["cartlist"]
        del request.session["total_money"]
        return HttpResponse("Y")
    except:
        return HttpResponse("N")

def detail(request, oid=1):
    """加载订单详情信息"""
    '''加载订单信息'''
    oid = request.GET.get("oid", 0)

    # 加载订单详情
    dlist = OrderDetail.objects.filter(order_id=oid)
    # 遍历每个商品详情，从Goods中获取对应的图片
    # for og in dlist:
    #    og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname

    # 放置模板变量，加载模板并输出
    context = {'detaillist': dlist}
    return render(request, "web/detail.html", context)

def status(request):
    """修改订单状态"""
    ''' 修改订单状态 '''
    try:
        oid = request.GET.get("oid", '0')
        ob = Orders.objects.get(id=oid)
        ob.status = request.GET['status']
        ob.save()
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")

