from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from board.models import Question, Answer, Comment
from board.forms import QuestionForm, AnswerForm, CommentForm

#def index(request): 연습!!
    #return HttpResponse("pyweb 사이트입니다")
    #season = '겨울'
    #season_list = ['봄', '여름', '가을', '겨울']
    #return render(request, 'board/question_list.html', {'season':season, 'season_list':season_list })

def index(request): #전체 페이지의 index
    return render(request, 'board/index.html')

def boardlist(request):
    #질문/답변의 index
    #질문 목록
    #question_list = Question.objects.all() #내가 만든 질문에 대한 db전체 조회
    #페이지 처리
    page = request.GET.get('page', 1) #127.0.0.1:8000/로 들어가면 기본 1페이지 보임
    kw = request.GET.get('kw', '') #검색어 가져오기
    #검색
    question_list = Question.objects.order_by('-create_date')  #최신 작성일 기준으로 내림차순으로 정렬 추가
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) | #제목 검색
            Q(content__icontains=kw) | #내용 검색
            Q(author__username__icontains=kw) | #질문 글쓴이 검색
            Q(answer__author__username__icontains=kw) | #답변 글쓴이 검색
            Q(answer__content__icontains=kw) #답변 글쓴이 검색
        ).distinct() #유일한 것 검색

    paginator = Paginator(question_list, 10) #페이지 당 10개씩 설정
    page_obj = paginator.get_page(page) #페이지 가져오기
    context = {'question_list':page_obj, 'page':page, 'kw':kw}
    return render(request, 'board/question_list.html', context)

def detail(request, question_id):
    #질문/답변 상세
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id) #경로에 오류가 있을 때 404(페이지가 없음, 에러는 아님)로 처리, pk는 0001_initial.py에서 id의 primary_key를 의미
    return render(request, 'board/detail.html', {'question':question})