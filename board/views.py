from django.http import HttpResponse
from django.shortcuts import render
from board.models import Question

#def index(request):
    #return HttpResponse("pyweb 사이트입니다")
    #season = '겨울'
    #season_list = ['봄', '여름', '가을', '겨울']
    #return render(request, 'board/question_list.html', {'season':season, 'season_list':season_list })

def index(request):
    question_list = Question.objects.all() #내가 만든 질문에 대한 db전체 조회
    return render(request, 'board/question_list.html',
                  {'question_list':question_list})

def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    return render(request, 'board/detail.html', {'question':question})