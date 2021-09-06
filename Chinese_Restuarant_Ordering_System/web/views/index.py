from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from myadmin.models import User, Shop, Category, Product

# Create your views here.


def webindex(request):
    """点餐前台首页"""
    # 获取购物车中菜品信息
    cartlist = request.session.get('cartlist', {})
    total_money = 0
    # 遍历购物车种商品的price信息，统计总金额
    for product in cartlist.values():
        total_money += product['num'] * product['price']
    request.session['total_money'] = total_money
    return render(request,'web/index.html')

def index(request):
    """将对index的访问转到web_index路由"""
    return redirect(reverse('web_index'))

def login(request):
    """加载登录表单页"""
    #加载可用的shop列表
    shoplist = Shop.objects.filter(status=1)
    context = {'shoplist': shoplist}
    return render(request,'web/login.html',context)

def dologin(request):
    """执行登录"""
    # 执行确认是否选择商铺校验
    shop_id = request.POST['shop_id']
    if shop_id == 0:
        return redirect(reverse('web_login') + "?errinfo=1")

    # 执行验证码校验，通过post拿到用户输入的验证码
    # 与session里的验证码真实值作比较
    if request.POST['verify'] != request.session['verifycode']:
        return redirect(reverse('web_login') + "?errinfo=2")

    try:
        #根据post上来的账号来获得user表中的登陆者信息
        user = User.objects.get(username=request.POST['username'])
        #判断当前用户状态是否为1（正常）或者6（管理员）：
        if user.status == 1 or user.status == 6:
            # 判断登录密码是否相同
            # 生成密码的反向操作
            import hashlib
            md5 = hashlib.md5()
            s = request.POST['password'] + user.password_salt
            # 上面一步：获取post表单中用户输入的密码以及数据库中该用户密码的干扰值
            # 组合在一起后进行md5的操作
            md5.update(s.encode('utf-8'))  # 用s生成md5
            if user.password_hash == md5.hexdigest():
                # 如果md5与数据库中该用户开始得到的password_hash值相同，则登陆成功
                # 将当前登录成功的用户信息以webuser为key写入到session
                # 这个'webuser'是我们在自己间中自己定义的label
                # .toDict()这个是在models中定义的方法，将user转成字典
                request.session['webuser'] = user.toDict()
                # 加载当前商铺信息
                shopob = Shop.objects.get(id=request.POST['shop_id'])
                request.session['shopinfo'] = shopob.toDict()
                # 获取当前店铺所对应的商品类别信息
                clist = Category.objects.filter(shop_id=shopob.id, status=1)
                categorylist = dict()
                productlist = dict()
                #遍历菜品类别信息
                for vo in clist:
                    c = {'id': vo.id, 'name': vo.name, 'pids': []}
                    plist = Product.objects.filter(shop_id=shopob.id, category_id=vo.id, status=1)
                    #遍历当前类别下的所有菜品信息
                    for p in plist:
                        c['pids'].append(p.toDict())
                        productlist[p.id] = p.toDict()
                    categorylist[vo.id] = c
                request.session['categorylist'] = categorylist  # 菜品类别列表
                request.session['productlist'] = productlist  # 菜品列表
                print('shopob=',shopob,'\n', categorylist,'\n', productlist)
                # 重定向到后台管理首页、
                return redirect(reverse('web_index'))

            else:
                return redirect(reverse('web_login')+"?errinfo=3")
        else:
            return redirect(reverse('web_login')+"?errinfo=5")
    except:
        return redirect(reverse('web_login')+"?errinfo=4")


def logout(request):
    """执行退出"""
    del request.session['webuser']
    return redirect(reverse("web_login"))

def verify(request):
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/Blazed.ttf', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

