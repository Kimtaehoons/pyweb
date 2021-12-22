from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from board.models import Question, Answer
from board.forms import QuestionForm, AnswerForm

#def index(request):
    #return HttpResponse("pyweb 사이트입니다")
    #season = '겨울'
    #season_list = ['봄', '여름', '가을', '겨울']
    #return render(request, 'board/question_list.html', {'season':season, 'season_list':season_list })

def index(request): #게시판(board)의 index(전체 페이지의 index가 아님)
    #질문 목록
    #question_list = Question.objects.all() #내가 만든 질문에 대한 db전체 조회
    question_list = Question.objects.order_by('-create_date') #최신 작성일 기준으로 내림차순으로 정렬 추가
    return render(request, 'board/question_list.html',
                  {'question_list':question_list})

def detail(request, question_id):
    #질문/답변 상세
    #question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id) #경로에 오류가 있을 때 404(페이지가 없음, 에러는 아님)로 처리, pk는 0001_initial.py에서 id의 primary_key를 의미
    return render(request, 'board/detail.html', {'question':question})

def question_create(request):
    #질문 등록
    if request.method == "POST": #POST방식
        form = QuestionForm(request.POST) #자료 전달받음(입력한 것을 form에 담음)
        if form.is_valid(): #유효성 검사
            question = form.save(commit=False) #임시 저장(form에서 넘어올 때, date가 넘어오지 않았기 때문에 False)
            question.create_date = timezone.now() #날짜/시간 저장
            question.save() #실제 저장
            return redirect('board:index') #이동 경로(app_name인 board) 저장
    else: #GET방식
        form = QuestionForm() #form객체 생성
    return render(request, 'board/question_form.html', {'form':form})

def answer_create(request, question_id):
    #답변 등록
    #question = Question.objects.get(id=question_id) #해당id의 질문 객체 생성
    question = get_object_or_404(Question, pk=question_id) 
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid(): #에러가 났을 때는 flask처럼 넘어가지는 않는다
            answer = form.save(commit=False) #입력한 내용만 저장
            answer.create_date = timezone.now()
            answer.question = question #위에서 해당id의 질문 객체 생성된 외래키 질문 저장
            answer.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question':question, 'form': form} #question은 GET, POST방식일 때 모두 보내져야하므로 밖으로 꺼내준다
    return render(request, 'board/detail.html', context)