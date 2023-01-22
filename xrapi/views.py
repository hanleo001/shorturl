from Third.settings import DOMAIN

from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponseRedirect
from xrapi import models
import hashlib
from django.contrib.auth import authenticate
from django.contrib.auth import login as lg
from django.contrib.auth import logout as lgo
from random import randint
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def setpassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    password = md5.hexdigest()
    return str(password)


def login(request):
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            lg(request, user)
            return redirect('/shorturl/')
        else:
            return render(request, 'selflogin.html', {'ss': '结果', 'rurl': '用户名或密码错误'})
    return render(request, "selflogin.html")


def logout(request):
    lgo(request)
    return redirect('/index/')


def root(request):
    return redirect('/index/')


def index(request):
    return render(request, 'selfindex.html')


def exist_surl(surl):
    used_url = ['login', '', 'index', 'shorturl', 'logout','register']
    if surl in used_url:
        return True
    if surl[0:5] == 'admin':
        return True
    surl_obj = models.Shorturl.objects.filter(surl=surl)
    if surl_obj:
        return True
    else:
        return False


def randurl():
    for i in range(5):
        default_surl = str(randint(100000, 999999))
        if exist_surl(default_surl):
            continue
        return default_surl
    raise OSError("无法生成随机url")


@login_required(login_url='/login/')
def shorturl(request):
    base_url = DOMAIN + '/'
    if request.method == 'POST' and request.POST.get('url'):
        default_url = randurl()
        surl = request.POST.get("surl") or default_url
        if exist_surl(surl):
            return render(request, 'shorturl.html', {'base_url': base_url, 'res': "您输入的短链接已占用"})
        url_obj = models.Shorturl(url=request.POST.get('url'), surl=surl)
        url_obj.created_user = request.user.username
        url_obj.save()
        rurl = base_url + surl + '/'
        return render(request, 'shorturl.html',
                      {'base_url': base_url, 'surl': surl, 'res': "成功生成", 'ss': '您生成的短链接为：', 'rurl': rurl})
    return render(request, 'shorturl.html', {'base_url': base_url})


def jump(request, surl):
    if exist_surl(surl):
        surl_obj = models.Shorturl.objects.filter(surl=surl)[0]
        surl_obj.click_times+=1
        surl_obj.save()
        return redirect(surl_obj.url)
    else:
        return render(request, 'no_url.html')


def register(request):
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        inv_code = request.POST.get('inv_code')
        inv_code_obj = models.Invitation_code.objects.filter(code=inv_code)
        if inv_code_obj:
            inv_code_obj = inv_code_obj[0]
            if inv_code_obj.timesused < inv_code_obj.timeslimit:
                inv_code_obj.timesused+=1
                inv_code_obj.save()
                User.objects.create_user(username=username, password=password, email=email)
                return render(request, 'register.html', {'ss': '结果', 'rurl': '注册成功'})
            return render(request, 'register.html', {'ss': "结果", "rurl": '邀请码已失效'})
        return render(request, 'register.html', {'ss': '结果','rurl': '邀请码不存在'})
    return render(request, "register.html")
