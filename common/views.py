from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from common.forms import UserForm

def signup(request):
    #회원 가입
    if request.method == "POST":
        form = UserForm(request.POST) #입력값을 가져옴
        if form.is_valid():
            form.save()  #실제 저장
            username = form.cleaned_data.get('username') #전달받은 사용자ID 가져옴
            password = form.cleaned_data.get('password1') #전달받은 비밀번호 가져옴
            user = authenticate(username=username, password=password) #세션(인증) 발급, auth모듈안에 authenticate()함수가 다 들어있음
            login(request, user) #login 실행, auth모듈안에 login()함수가 다 들어있음
            return redirect('board:index')
    else:
        form = UserForm() #비어있는 새폼,
    return render(request, 'common/signup.html', {'form':form})
