from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from board.models import Question, Answer, Comment
from board.forms import QuestionForm, AnswerForm, CommentForm

@login_required(login_url='common:login') #로그인 안 돼있으면 로그인 페이지로 보냄(즉, 답변 권한은 로그인 한 사람에게 부여)
def answer_create(request, question_id):
    #답변 등록
    #question = Question.objects.get(id=question_id) #해당id의 질문 객체 생성
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid(): #에러가 났을 때는 flask처럼 넘어가지는 않는다
            answer = form.save(commit=False) #입력한 내용만 저장
            answer.create_date = timezone.now()
            answer.author = request.user
            answer.question = question #위에서 해당id의 질문 객체 생성된 외래키 질문 저장
            answer.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question':question, 'form': form} #question은 GET, POST방식일 때 모두 보내져야하므로 밖으로 꺼내준다
    return render(request, 'board/detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    #답변 수정
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('board:detail', question_id=answer.question_id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'board/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    #답변 삭제
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()
    return redirect('board:detail', question_id=answer.question_id)