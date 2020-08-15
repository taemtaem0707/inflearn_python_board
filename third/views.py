from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from third.models import Restaurant, Review
from third.forms import RestaurantForm, ReviewForm, updateRestaurantForm
from django.http import HttpResponseRedirect
import math
from django.db.models import Count, Avg


# Create your views here.
def list(request):
    # annotate에서 review는 모델명, review__point는 모델의 point를 의미
    restaurant = Restaurant.objects.all().annotate(reviews_count=Count('review'))\
        .annotate(average_point=Avg('review__point'))
    paginator = Paginator(restaurant, 5)

    page = request.GET.get('page')
    if page == None:
        page = 1

    # 시작페이지, 끝 페이지 구하기
    page_F = float(page)
    if page_F <= 10:
        beginPage = 1
    else:
        beginPage = (math.trunc(page_F / 10)) * 10 + 1

    if (beginPage + 10) > paginator.num_pages:
        lastPage = paginator.num_pages
    else:
        lastPage = beginPage + 9
    nextRangeStartPage = lastPage + 1

    pageRange = []
    for num in range(beginPage, lastPage+1):
        pageRange.append(num)

    items = paginator.get_page(page)

    context = {
        'restaurants': items,
        'lastPage': lastPage,
        'pageRange': pageRange,
        'nextRangeStartPage': nextRangeStartPage,
    }
    return render(request, 'third/list.html', context)


def create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return HttpResponseRedirect('/third/list')
    form = RestaurantForm()
    return render(request, 'third/create.html', {'form':form})


def update(request, id):
    if id is not None:
        if request.method == 'POST' and 'id' in request.POST:
            item = get_object_or_404(Restaurant, pk=id) # id에 해당하는 모델 데이터 가져오기
            password = request.POST.get('password','') # 사용자 입력 패스워드 값
            form = updateRestaurantForm(request.POST, instance=item) # 입력할 폼
            if form.is_valid() and password == item.password:
                item = form.save()
        elif request.method =='GET':
            item = get_object_or_404(Restaurant, pk=id)
            form = RestaurantForm(instance=item)
            context = {
                'form':form,
                'id':item.id
            }
            return render(request, 'third/update.html', context)
        return HttpResponseRedirect('/third/list/')
    return HttpResponseRedirect('/third/list/')


# urls에서 <int:id>를 통해 id가 넘어옴:
def detail(request, id):
    if id is not None:
        item = get_object_or_404(Restaurant, pk=id)
        # 현재 레스토랑에 해당하는 review의 모든 정보를 가져오기
        reviews = Review.objects.filter(restaurant=item).all()
        return render(request, 'third/detail.html', {'item' : item, 'reviews':reviews})
    return HttpResponseRedirect('/third/list/')


def delete(request, id):
    item = get_object_or_404(Restaurant, pk=id)
    if request.method == 'POST' and 'password' in request.POST: # POST로 받고 패스워드도 전달받았을 때
        print(item.password)
        if item.password == request.POST.get('password') or item.password is None:
            item.delete()
            return redirect('list')
        return redirect('restaurant-detail', id=id)
    return render(request, 'third/delete.html', {'item':item})


def review_create(request, restaurant_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_item = form.save()
        return redirect('restaurant-detail', id=restaurant_id)

    item = get_object_or_404(Restaurant, pk=restaurant_id)
    # 빈 form값이 아닌 사전에 정의한 내용이름 입력
    # 해당 부분에서는 미리 hiddenfield에 'restaurant'를 넣기 위해 사용
    form = ReviewForm(initial={'restaurant':item})
    return render(request, 'third/review_create.html', {'form':form, 'item':item})


def review_delete(request, restaurant_id, review_id):
    item = get_object_or_404(Review, pk=review_id)
    item.delete()

    return redirect('restaurant-detail', id=restaurant_id)


# 조인사용
def review_list(request):
    reviews = Review.objects.all().select_related().order_by('-created_at')
    paginator = Paginator(reviews, 10)

    page = request.GET.get('page')
    items = paginator.get_page(page)

    context = {
        'reviews':items
    }

    return render(request, 'third/review_list.html', context)