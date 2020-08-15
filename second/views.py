from django.shortcuts import render
# 특정 http로 전송
from django.http import HttpResponseRedirect
# second.models의 Post를 호출
from second.models import Post
# forms.py에서 PostForm 호출
from .forms import PostForm


# Create your views here.

def list(request):
    context = {
        'items': Post.objects.all()
    }
    return render(request, 'second/list.html', context)


def create(request):
    if request.method == 'POST': # post라면
        form = PostForm(request.POST) # form.py에서 가져온 PostForm
        if form.is_valid(): # form 값이 유효하다면
           new_item = form.save()  # post로 전달된 데이터 값들이 모두 연결된 model에 자동으로 저장
        return HttpResponseRedirect('/second/list/')  # 유효한 값이 없다면 create로 페이지 이동
    form = PostForm() #  get일 경우 진행
    return render(request, 'second/create.html', {'form':form}) # create.html로 forms의 PostForm 양식을 전송


def confirm(request):
    form = PostForm(request.POST) # 포스트로 받는 것
    if form.is_valid(): # 만약 form으로 받은 값이 유효하다면
        return render(request, 'second/confirm.html', {'form':form}) # 해당 페이지로 이동
