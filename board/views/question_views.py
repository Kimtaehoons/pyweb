from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from board.models import Question, Answer, Comment
from board.forms import QuestionForm, AnswerForm, CommentForm

@login_required(login_url='common:login')
def question_create(request):
    #질문 등록
    if request.method == "POST": #POST방식
        form = QuestionForm(request.POST) #자료 전달받음(입력한 것을 form에 담음)
        if form.is_valid(): #유효성 검사
            question = form.save(commit=False) #임시 저장(form에서 넘어올 때, date가 넘어오지 않았기 때문에 False)
            question.create_date = timezone.now() #날짜/시간 저장
            question.author = request.user #추가한 칼럼인 글쓴이에 세션(request.user) 저장
            question.save() #실제 저장
            return redirect('board:boardlist') #이동 경로(app_name인 board) 저장
    else: #GET방식
        form = QuestionForm() #form객체 생성
    return render(request, 'board/question_form.html', {'form':form})

@login_required(login_url='common:login')
def question_modify(request, question_id):
    #질문 수정
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False) #수정된 질문 임시 저장
            question.author = request.user #세션 발급
            question.modify_date = timezone.now() #수정일
            question.save()
            return redirect('board:detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question) #instance를 쓰면 폼에 내용이 채워짐
    return render(request, 'board/question_form.html', {'form':form})

@login_required(login_url='common:login')
def question_delete(request, question_id):
    #질문 삭제
    question = get_object_or_404(Question, pk=question_id) #질문 가져와서
    question.delete() #질문 삭제
    return redirect('board:index')