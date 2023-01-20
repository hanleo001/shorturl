from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponseRedirect
from xrapi import models
import hashlib
from django.contrib.auth import authenticate
from django.contrib.auth import login as lg
from django.contrib.auth import logout as lgo
from random import randint
from django.contrib.auth.decorators import login_required


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
    if request.method == 'POST' and request.POST.get('url'):
        default_url = randurl()
        surl = request.POST.get("surl") or default_url
        if exist_surl(surl):
            return render(request, 'shorturl.html', {'res': "您输入的短链接已占用"})
        url_obj = models.Shorturl(url=request.POST.get('url'), surl=surl)
        url_obj.created_user = request.user.username
        url_obj.save()
        rurl = 'https://t.leoh.top/a/' + surl + '/'
        return render(request, 'shorturl.html',
                      {'surl': surl, 'res': "成功生成", 'ss': '您生成的短链接为：', 'rurl': rurl})
    return render(request, 'shorturl.html')


def jump(request, surl):
    if exist_surl(surl):
        surl_obj = models.Shorturl.objects.filter(surl=surl)[0]
        return redirect(surl_obj.url)
    else:
        return render(request, 'no_url.html')
