from django.urls import path
from board import views

app_name = 'board' #네임 스페이스 설정

urlpatterns = [
    #127.0.0.1:8000/board/
    path('', views.index, name='index'), #질문 목록/네임 스페이스 설정에 따른 name=''설정
    path('<int:question_id>/', views.detail, name='detail'), #질문/답변 상세보기
    path('question/create', views.question_create, name='question_create'), #질문 등록
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'), #답변 등록
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'), #질문 수정
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'), #질문 삭제
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'), #답변 수정
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'), #답변 삭제
]