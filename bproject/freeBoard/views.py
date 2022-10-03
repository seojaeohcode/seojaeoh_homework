from datetime import datetime
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render,redirect
from member.models import Member
from freeBoard.models import Fboard
from django.db.models import F,Q
from django.core.paginator import Paginator
# Create your views here.
def fboardList(request):
    qs = Fboard.objects.order_by('-b_group','b_step')
    paginator = Paginator(qs,10)
    nowpage = int(request.GET.get('nowpage',1))
    qs = paginator.get_page(nowpage)
    context={'fboardList':qs, 'nowpage':nowpage}
    return render(request,'fboardList.html', context)

def fboardSearch(request):
    category = request.POST.get('category')
    sword = request.POST.get('sword')
    if category=='all':
        qs = Fboard.objects.filter(Q(b_title__contains=sword)|Q(b_content__contains=sword))
    elif category == 'title':
        # content검색
        qs = Fboard.objects.filter(b_title__contains=sword)
    else:
        # content검색
        qs = Fboard.objects.filter(b_content__contains=sword)
    context={"fboardList":qs,"category":category,"sword":sword}
    return render(request,'fboardList.html',context) 

def fboardDelete(request,b_no):
    qs = Fboard.objects.get(b_no=b_no)
    qs.delete()
    return redirect('freeBoard:fboardList')

def fboardWrite(request):
    if request.method == 'GET':
        return render(request, 'fboardWrite.html')
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
        return redirect('freeBoard:fboardList')

def fboardView(request, b_no):
    qs = Fboard.objects.get(b_no=b_no)
    context = {"fboard":qs}
    return render(request, 'fboardView.html', context)

def fboardUpdate(request, b_no):
    if request.method=='GET':
        qs = Fboard.objects.get(b_no=b_no)
        context = {"fboard":qs}
        print("views :",b_no)
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
            qs.b_file = b_file
        qs.save()
        return redirect('freeBoard:fboardList')
    
def fboardReply(request,b_no):
    if request.method == 'GET':
        qs = Fboard.objects.get(b_no=b_no)
        context = {"fboard":qs}
        print("views :",b_no)
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
        return redirect('freeBoard:fboardList')