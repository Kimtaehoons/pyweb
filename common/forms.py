from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm): #이미 부모필드에는 username, password1, password2가 있음(UserCreationForm에 ctrl+마우스 올려둬서 dictionary에서 확인 가능)
    email = forms.EmailField() 
    class Meta:
        model = User
        fields = ('username', 'email') #UserCreationForm을 상속받은 필드 외에 추가할 필드를 튜플 구조로