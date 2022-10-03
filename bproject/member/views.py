from django.shortcuts import redirect, render

from member.models import Member

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        try:
            qs = Member.objects.get(id=id, pw=pw)
            request.session['session_id'] = qs.id
            request.session['session_name'] = qs.name
            return redirect("/")
        except:
            context={"msg":'아이디,패스워드가 잘못됨.'}
            return render(request,'login.html',context)
        
def logout(request):
    request.session.clear()
    return redirect('/')

def join01(request):
    return render(request, 'join01.html')

def join02(request):
    return render(request, 'join02.html')

def join03(request):
    return render(request, 'join03.html')