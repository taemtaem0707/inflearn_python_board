from django.shortcuts import render
from django.http import HttpResponse

from django.template import loader
from datetime import datetime

import random

# Create your views here.
# 첫 화면
def index(request):
    now = datetime.now() # 현재시간을 불러오는 메소드
    context = {
        'current_date':now,
    }
    return render(request, 'first/index.html', context)


def select(request):
    context = {

    }
    return render(request, 'first/select.html', context)


def result(request):
    # select.html로부터 get방식으로 number를 전해받음
    chosen = int(request.GET['number'])

    results = []
    if chosen >= 1 and chosen <= 45:
        results.append(chosen)

    box = []
    for i in range(0, 45):
        if chosen != i+1:
            box.append(i+1)

    random.shuffle(box)

    while len(results) < 6:
        results.append(box.pop())

    context = {
        'numbers':results
    }
    return render(request, 'first/result.html', context)