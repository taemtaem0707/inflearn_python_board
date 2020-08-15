from django.urls import path

from . import views

# urls -> views와 연결
urlpatterns = [
    path('', views.index, name='index'),
    path('select/', views.select, name='select'),
    path('result/', views.result, name='result'),





    #re_path(r'^select/(?P<year>[0-9]{4})/$') # 정규표현식으로 사용 가능
    #                                           정규표현식 테스트 https://regex101.com/
    #path('select/<int:year>/')  # <int:> <str:> <slug:>
    #                              숫자    문자    - _ 영,숫자,문자
]