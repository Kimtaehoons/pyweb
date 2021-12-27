from django.contrib.auth.models import User
from django.db import models

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) #User(common의 User)는 직접 만든 것이 아니고 가져다가 쓴 것(그래서 총 3개의 class가 있음)
    subject = models.CharField(max_length=100) #제목 칼럼
    content = models.TextField() #질문 내용
    create_date = models.DateTimeField() #질문 작성일
    modify_date = models.DateTimeField(null=True, blank=True) #질문 수정일 / null=True는 "매번 수정 안 할 수 있다", blank=True는 "웹 상에서 form이 비어있을 수 있다"

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #외래키, 질문이 삭제되면 답변도 같이 삭제 / 제목 칼럼
    content = models.TextField() #답변 내용
    create_date = models.DateTimeField() #답변 작성일
    modify_date = models.DateTimeField(null=True, blank=True) #답변 수정일

    def __str__(self):
        return self.content
