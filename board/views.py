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

@login_required(login_url='common:login')
def vote_question(request, question_id):
    #질문 추천
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        question.voter.add(request.user) #추천 추가(로그인한 사람)
    return redirect('board:detail', question_id=question.id)

@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    #질문 댓글 등록
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST) #입력된 댓글 내용(채워진 폼)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user #세션 권한
            comment.create_date = timezone.now()
            comment.question = question #참조 외래키
            comment.save() #실제 저장
            return redirect('board:detail', question_id=question.id)
    else:
        form = CommentForm() #빈 폼(댓글 추가버튼을 눌렀을 때 작성할 수 있는 빈 폼이 뜬다)
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    #질문 댓글 삭제
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('board:detail', question_id=comment.question.id)

@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    #질문 댓글 수정
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment) #변경된 입력 내용
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('board:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment) #질문 댓글 폼에 채워진 폼으로 가져옴
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)
