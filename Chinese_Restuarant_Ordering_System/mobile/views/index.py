from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from myadmin.models import Member, Shop, Category, Product
from myadmin.models import Orders, OrderDetail, Payment
from datetime import datetime


# Create your views here.

def index(request):
    #移动端首页
    #获取并判断当前是否有店铺信息
    shopinfo = request.session.get("shopinfo",None)
    if shopinfo is None:
        return redirect(reverse('mobile_shop'))

    #获取当前店铺下的菜品类别和菜品信息
    clist = Category.objects.filter(shop_id=shopinfo['id'],status=1)
    productlist = dict()
    for vo in clist:
        plist = Product.objects.filter(category_id=vo.id,status=1)
        productlist[vo.id] = plist
    context = {"categorylist":clist,"productlist":productlist.items(),'cid':clist[0]}

    return render(request,"mobile/index.html",context)

def register(request):
    #移动端会员注册登录表单
    return render(request,"mobile/register.html")

def doregister(request):
    #执行会员登录
    #模拟短信验证
    verifycode = '1234' #request.session['verifycode']
    if verifycode != request.POST['code']:
        context = {'info':'短信验证码错误！'}
        return render(request,"mobile/register.html",context)
    #根据号码获取当前会员信息
    try:
        member = Member.objects.get(mobile=request.POST['mobile'])
        #若存在则检验当前会员状态
        if member.status == 1:
            #将当前会员信息转成字典格式并存放到session中
            request.session['mobileuser'] = member.toDict()
            return redirect(reverse('mobile_index'))

        else:
            context = {'info':'该账户已经被禁用！'}
            return render(request,"mobile/register.html",context)

    except:
        #若报错的话就进行当前会员的注册操作
        om = Member()
        om.nickname = '游客'
        om.mobile = request.POST['mobile']
        om.avatar = 'moren.png'
        om.status = 1
        om.save()
        # 将当前会员信息转成字典格式并存放到session中
        request.session['mobileuser'] = om.toDict()
        return redirect(reverse('mobile_index'))


def shop(request):
    #店铺选择
    context = {'shoplist':Shop.objects.filter(status=1)}
    return render(request,"mobile/shop.html",context)

def selectshop(request):
    #移动端首页
    #获取选择的店铺信息
    sid = request.GET['sid']
    ob = Shop.objects.get(id=sid)
    request.session['shopinfo'] = ob.toDict()
    request.session['cartlist'] = {}
    #跳转到首页
    return redirect(reverse('mobile_index'))


def addorders(request):
    """移动端下单页"""
    #从sesion中获取cartlist表单若没有则返回{}
    cartlist = request.session.get('cartlist',{})
    total_money = 0
    for vo in cartlist.values():
        total_money += vo['num'] * vo['price']

    request.session['total_money'] = total_money
    return render(request,"mobile/addorders.html")

def doaddorders(request):
    """执行订单添加"""
    try:
        #对orders表执行添加操作
        od = Orders()
        od.shop_id = request.session['shopinfo']['id'] #店铺id号
        od.member_id = request.session['mobileuser']['id']
        od.user_id = 0
        od.money = request.session['total_money']
        od.status = 1  #订单状态:1过行中/2无效/3已完成
        od.payment_status = 2  #支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        #对payment表执行添加操作
        op = Payment()
        op.order_id = od.id
        op.member_id = request.session['mobileuser']['id']
        op.type = 1 #付款方式：1会员付款/2收银收款
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

    except Exception as err:
        print(err)

    return render(request,'mobile/orderinfo.html',{"order":od})
