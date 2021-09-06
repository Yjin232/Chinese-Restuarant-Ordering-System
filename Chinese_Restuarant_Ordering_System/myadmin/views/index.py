from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.

#后台管理首页
def index(request):
    return render(request,'myadmin/index/index.html')

#后台管理员登录页
def login(request):
    return render(request,'myadmin/index/login.html')

#执行管理员登录
def dologin(request):
    try:
        # 执行验证码校验,这里post拿到的是用户输入的验证码，
        # session里得到的是每次随机生成验证码后塞进session表中的验证码真实值
        if request.POST['verify'] != request.session['verifycode']:
            context = {'info': "The verification code doesn't match!"}
            return render(request, 'myadmin/index/login.html', context)
        #根据登录账号获取登陆者信息
        user =User.objects.get(username=request.POST['username'])
        #判断当前用户是否是管理员
        if user.status == 6:
            #判断登录密码是否相同
            # 生成密码的反向操作
            import hashlib
            md5 = hashlib.md5()
            s = request.POST['password'] + user.password_salt
            # 上面一步：获取post表单中用户输入的密码以及数据库中该用户密码的干扰值
            # 组合在一起后进行md5的操作
            md5.update(s.encode('utf-8'))  # 用s生成md5
            if user.password_hash == md5.hexdigest():
                #如果md5与数据库中该用户开始得到的password_hash值相同，则登陆成功
                #将当前登录成功的用户信息以adminuser为key写入到session
                #这个'adminuser'是我们在自己间中自己定义的label
                #.toDict()这个是在models中定义的方法，将user转成字典
                request.session['adminuser'] = user.toDict()
                #重定向到后台管理首页
                return redirect(reverse("myadmin_index"))
            else:
                context = {'info': 'Wrong Password!'}

        else:
            context = {'info': 'Invalid Username!'}

    except:
        context = {'info':"Username not exists！"}
    #若报错则跳转回登录界面
    return render(request,'myadmin/index/login.html',context)

#执行管理员退出
def logout(request):
    del request.session['adminuser']
    return redirect(reverse("myadmin_login"))

#验证码模块
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