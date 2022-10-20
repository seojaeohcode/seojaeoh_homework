from datetime import datetime
from django.shortcuts import render,redirect
from freeBoard.models import Revenue
from member.models import Member
from freeBoard.models import Comment, Fboard
from django.db.models import F,Q
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests

def chart01(request):
    return render(request, 'chart01.html')

@csrf_exempt
def chartData(request):
    qs = Revenue.objects.all()
    chartList = list(qs.values())
    return JsonResponse(chartList, safe=False)

@csrf_exempt
def chartList(request):
    public_key ='918RE13GA7OY7ZEmUzApgbOeAcQoZ%2FaHsXWcqPAKQ9YNNPj83KOstRMRIUrCFIAcm9qj2R6b7NFZjp%2FYsYzJLg%3D%3D'
    resultType ='json'
    url = 'http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey={}&numOfRows=10&pageNo=1&resultType={}'.format(public_key,resultType)
    res = requests.get(url)
    json_res = json.loads(res.text)
    publicList = json_res['response']['body']['items']['item']
    nlist = [1,2,3,4,5]
    
    return JsonResponse(publicList, safe=False)

# 공공데이터 리스트
def publicList(request):
    public_key ='918RE13GA7OY7ZEmUzApgbOeAcQoZ%2FaHsXWcqPAKQ9YNNPj83KOstRMRIUrCFIAcm9qj2R6b7NFZjp%2FYsYzJLg%3D%3D'
    resultType ='json'
    url = 'http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey={}&numOfRows=10&pageNo=1&resultType={}'.format(public_key,resultType)
    res = requests.get(url)
    json_res = json.loads(res.text)
    publicList = json_res['response']['body']['items']['item']
    numOfRows = json_res['response']['body']['numOfRows']
    context={'publicList':publicList,"numOfRows":numOfRows}
    
    return render(request,'publicList.html',context)

@csrf_exempt
def commPost(request):
    test = request.POST.get("test")
    context = {"msg":"데이터전송이 잘되었습니다." }
    return JsonResponse(context)


def commDelete(request):
    c_no = request.GET.get('c_no')
    qs = Comment.objects.get(c_no=c_no)
    qs.delete()
    context={'msg':"댓글이 삭제되었습니다."}
    return JsonResponse(context)

def commUpdate(request):
    c_no = request.GET.get('c_no')
    c_content = request.GET.get('c_content')
    id = request.session.get('session_id')
    qs = Comment.objects.get(c_no=c_no)
    qs.c_content = c_content
    qs.c_date = datetime.now()
    qs.save()
    
    context={"c_no":c_no,"c_content":c_content,"c_date":qs.c_date}
    return JsonResponse(context)
    
def commWrite(request):
    id = request.session.get('session_id')
    member = Member.objects.get(id=id)
    b_no = request.GET.get('b_no')
    fboard = Fboard.objects.get(b_no=b_no)
    c_pw = request.GET.get('c_pw')
    c_content = request.GET.get('c_content')
    
    qs = Comment(member=member,fboard=fboard,c_pw=c_pw,c_content = c_content)
    qs.save()
    c_no = qs.c_no
    c_date = qs.c_date
    
    context={"c_no":c_no,"b_no":b_no,"c_pw":c_pw,"c_content":c_content,"c_date":c_date}
    return JsonResponse(context) 
    
def commList(request):
    b_no = request.GET.get('b_no')
    comm_qs = Comment.objects.filter(fboard=b_no).order_by('-c_no')
    clist = list(comm_qs.values())
    
    return JsonResponse(clist,safe=False)
    
def event(request):
    qs = Fboard.objects.order_by('-b_group','b_step')  
    
    paginator = Paginator(qs,3)  
    qs = paginator.get_page(1)  
    
    context={"fboardList":qs}
    return render(request,'event.html',context)

def eventView(request,b_no):
    qs = Fboard.objects.get(b_no=b_no)
    qs.b_hit += 1  
    qs.save()
    comm_qs = Comment.objects.filter(fboard=b_no).order_by('-c_no')
    count = comm_qs.count()
    context = {"fboard":qs,"commList":comm_qs,"commCount":count}
    return render(request,'eventView.html',context)

def fboardReply(request,nowpage,category,sword,b_no):
    if request.method == 'GET':
        qs = Fboard.objects.get(b_no=b_no)
        context = {"fboard":qs,"nowpage":nowpage,"category":category,"sword":sword}
        return render(request,'fboardReply.html',context)
    else:
        id = request.session['session_id'] 
        member = Member.objects.get(id=id)
        b_no = request.POST.get("no")
        b_group = int(request.POST.get("group"))  
        b_step = int(request.POST.get("step"))    
        b_indent = int(request.POST.get("indent")) 
        
        b_title = request.POST.get("title")
        b_content = request.POST.get("content")
        b_file = request.FILES.get('file',None)
        
        Fboard.objects.filter(b_group=b_group,b_step__gt=b_step).update\
            (b_step=F('b_step')+1)
        
        qs = Fboard(member=member,b_title=b_title,b_content=b_content,\
            b_group=b_group,b_step=b_step+1,b_indent=b_indent+1,b_file=b_file)
        qs.save()
        return redirect('freeBoard:fboardList', nowpage,category,sword)

def fboardDelete(request,nowpage,category,sword,b_no):
    qs = Fboard.objects.get(b_no=b_no)
    qs.delete()
    return redirect('freeBoard:fboardList', nowpage,category,sword)


def fboardUpdate(request,nowpage,category,sword,b_no):
    if request.method=='GET':
        qs = Fboard.objects.get(b_no=b_no)
        context = {"fboard":qs,"nowpage":nowpage,"category":category,"sword":sword}
        return render(request,'fboardUpdate.html',context)
    else:
        b_title = request.POST.get('title')
        b_content = request.POST.get('content')
        b_file = request.FILES.get('file',None)
        re_file = request.POST.get('refile')
        qs = Fboard.objects.get(b_no=b_no)
        qs.b_title = b_title
        qs.b_content = b_content
        qs.b_date = datetime.now()
        if b_file:
            qs.b_file=b_file
        qs.save()
        
        return redirect('freeBoard:fboardList', nowpage,category,sword)
        
def fboardView(request,nowpage,category,sword,b_no):
    qs = Fboard.objects.get(b_no=b_no)
    qs.b_hit += 1  
    qs.save()
    
    try:
        qs_prev = Fboard.objects.filter(b_group=qs.b_group,b_step__lt=qs.b_step).order_by('-b_group','b_step').last().b_no
    except:
        try:
            qs_prev = Fboard.objects.filter(b_group__gt=qs.b_group).order_by('-b_group','b_step').last().b_no
        except:
            qs_prev = Fboard.objects.order_by('-b_group','b_step').first().b_no
    try:
        qs_next = Fboard.objects.filter(b_group=qs.b_group,b_step__gt=qs.b_step).order_by('-b_group','b_step').first().b_no
    except:
        try:
            qs_next = Fboard.objects.filter(b_group__lt=qs.b_group).order_by('-b_group','b_step').first().b_no
        except:
            qs_next = Fboard.objects.order_by('-b_group','b_step').last().b_no    
    
    qsPrevData = Fboard.objects.get(b_no=qs_prev)
    qsNextData = Fboard.objects.get(b_no=qs_next)
    
    context = {"fboard":qs,'fboardPrev':qsPrevData,'fboardNext':qsNextData,'nowpage':nowpage,"category":category,"sword":sword}
    return render(request,'fboardView.html',context)

def fboardList(request,nowpage,category,sword):
    if request.method == "POST":
       ncategory = request.POST.get('category') 
       nsword = request.POST.get('sword')    
       category = ncategory
       sword = nsword
    if category=='1' and sword =='1':
        qs = Fboard.objects.order_by('-b_group','b_step')
    else:
        if category=='all':
            qs = Fboard.objects.filter(Q(b_title__contains=sword)|Q(b_content__contains=sword))
        elif category == 'title':
            qs = Fboard.objects.filter(b_title__contains=sword)
        else:
            qs = Fboard.objects.filter(b_content__contains=sword)    
    paginator = Paginator(qs,10) 
    qs = paginator.get_page(nowpage) 
    
    context={"fboardList":qs,"category":category,"sword":sword,"nowpage":nowpage}
    return render(request,'fboardList.html',context)     

def fboardWrite(request,nowpage,category,sword,):
    if request.method == 'GET':
        context={"nowpage":nowpage,"category":category,"sword":sword}
        return render(request,'fboardWrite.html',context)
    else:
        id = request.session['session_id']
        member = Member.objects.get(id=id)
        b_title = request.POST.get("title")
        b_content = request.POST.get("content")
        b_file = request.FILES.get('file',None)
        
        qs = Fboard(member=member,b_title=b_title,b_content=b_content,b_file=b_file)
        qs.save()
        qs.b_group = qs.b_no
        qs.save()
        return redirect('freeBoard:fboardList', nowpage,category,sword)