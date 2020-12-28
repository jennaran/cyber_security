from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account, Secret, Session
from django.db import connection


def getUser(request):
    sessionId = request.COOKIES.get('session_id')
    session = Session.objects.filter(id=sessionId).first()
    if(session is None):
        return None
    return session.account


def homePageView(request):
    user = getUser(request)
    if(user is None):
        return redirect('/login')
    secrets = Secret.objects.filter(owner=getUser(request))
    return render(request, 'pages/index.html', {'secrets': secrets, 'user': user})


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        account = Account.objects.filter(username=username).first()

        if account is not None and account.password == password:
            session = Session(account=account)
            session.save()

            response = redirect('/')
            response.set_cookie(key='session_id', value=session.id)
            return response
        else:
            html = "<p>There might not be account called %s</p>" % username
            return HttpResponse(html)
    return render(request, 'pages/login.html')


def addView(request):
    owner = getUser(request)
    if owner is not None:
        if request.method == 'POST':
            secret = request.POST.get('secret').strip()
            s = Secret(owner=owner, secret=secret)
            s.save()
    return redirect('/')


def secretView(request):
    if request.method == 'POST':
        secret_id = request.POST.get('secret_id').strip()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM pages_secret WHERE id=" + secret_id)
            secret = cursor.fetchone()
            if secret is not None:
                return render(request, 'pages/secret.html', {'secret': secret[1]})
    return redirect("/")

def logoutView(request):
    response = redirect('/')
    response.delete_cookie('session_id')
    return response
