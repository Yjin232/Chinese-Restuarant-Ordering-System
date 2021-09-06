from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Orders, OrderDetail, Payment, Shop, User, Product, Category


# Create your views here.

def index(request):
    #移动端个人中心首页
    return render(request,"mobile/member.html")


def orders(request):
    #移动端个人中心游览订单
    """游览信息"""
    omod = Orders.objects
    mid = request.session["mobileuser"]["id"]  # 获取当前会员id号
    olist = omod.filter(member_id=mid)
    mywhere = []  # 保存搜索条件状态

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        olist = olist.filter(status=status)
        mywhere.append("status=" + status)

    list2 = olist.order_by("id")
    orders_status = ['None','Waitlist','Invalid','Completed']

    for vo in list2:
        plist = OrderDetail.objects.filter(order_id=vo.id)[:4]
        vo.plist = plist
        vo.statusinfo = orders_status[vo.status]

    context = {'orderslist': list2}
    return render(request, 'mobile/member_orders.html', context)

def detail(request):
    ''' 个人中心中的订单详情 '''
    pid = request.GET.get("pid",0)
    order = Orders.objects.get(id=pid)

    order_status = ['None','Waitlist','Invalid','Completed']
    #获取关联其他表数据（订单详情，店铺信息）
    plist = OrderDetail.objects.filter(order_id=order.id)
    order.plist = plist
    shop = Shop.objects.only("name").get(id=order.shop_id)
    order.shopname = shop.name
    order.statusinfo = order_status[order.status] #转换订单状态

    return render(request,"mobile/member_detail.html",{"order":order})


def logout(request):
    #会员退出
    del request.session['mobileuser']
    return render(request,"mobile/register.html")

