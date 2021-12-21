from django import forms
from board.models import Question, Answer

#질문 등록 폼 만들기
class QuestionForm(forms.ModelForm):
    class Meta: #내부클래스, 중첩클래스
        model = Question
        fields = ['subject', 'content']
        #labels = { #question_form.html에서 {{ form.as_p }} 자동 질문 폼 생성하는 템플릿 태그에 해당하는 내용
            #'subject':'제목',
            #'content':'내용',
        #}

#답변 등록 폼 만들기
class AnswerForm(forms.ModelForm):
    class Meta:  # 내부클래스, 중첩클래스
        model = Answer
        fields = ['content']
        labels = {
            'content': '내용',
        }