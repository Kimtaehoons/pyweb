from django.urls import path
from django.contrib.auth import views as auth_views
from common import views

app_name = 'common'

urlpatterns = [ #클래스 제네릭 뷰로 기존에 입력된 클래스를 꺼내쓰는 방법과 직접 함수를 정의해서 쓰는 방법(모듈, 함수 사용하지 않음), 두 가지가 있다
    #LoginView 클래스(제네릭 뷰)를 사용하면 제어함수를 만들지 않음
    #로그 인
    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'), name='login'),
    #로그 아웃
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #회원 가입, 함수로 만들어서 사용(views.py에 제어함수 정의)
    path('signup/', views.signup, name='signup'),
]