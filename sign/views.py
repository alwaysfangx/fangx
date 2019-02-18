from django.shortcuts import render,get_list_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Guest,Event
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

def index(request):
    return render(request,'index.html')

#登陆动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password', '')
        user = auth.authenticate(username = username,password = password)
        if user is not None:
        #if username == 'admin' and password == 'admin123':
            auth.login(request,user)
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            #response.set_cookie('user',username,3600)
            return response
        else:
            return render(request,'index.html',{'error':'用户名or密码不对'})

#发布会管理
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    #username = request.COOKIES.get('user','')
    username = request.session.get('user', '')
    return render(request,"event_manage.html",{"user":username,"event":event_list})

@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get("name","")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,"event_manage.html",{"uesr":username,"events":event_list})

@login_required
def guest_manage(request):
    username = request.session.get('user','')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request,"guest_manage.html",{"user":username,"guests":contacts})

@login_required
def sign_index(request,eid):
    event = get_list_or_404(Event,id=eid)
    return render(request,'sign_index.html',{'event',event})