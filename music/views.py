from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Music
from django.db.models import Q
import random


def index(request):
    return render(request, 'music/index.html')


def detail(request, id):
    # get_object_or_404() 抛出404错误的快捷方式
    music = get_object_or_404(Music, pk=id)

    return render(request, 'music/detail.html', {'music': music})


def results(request):
    return render(request, 'music/result.html')


def search(request):
    # 获取到用户提交的搜索关键词
    search_text = request.GET['search_text']
    print(search_text)
    if not search_text:
        return render(request, 'music/index.html')
    # 多个条件查找，两种方式
    # reponse_list = Music.objects.filter(name__icontains=search_text) | Music.objects.filter(
    #     singer__icontains=search_text)
    reponse_list = Music.objects.filter(Q(name__icontains=search_text) | Q(singer__icontains=search_text))
    # response_list的类型是：<class 'django.db.models.query.QuerySet'>

    # 记录搜索数据，以后可能用到
    with open('record.txt', 'a', encoding='utf-8') as fp:
        if not reponse_list:
            fp.write('\n' + search_text + '\t0')  # 数据库中没有，0
        else:
            fp.write('\n' + search_text + '\t1')  # 数据库中存在 1
    return render(request, 'music/result.html', {'reponse_list': reponse_list})


def good_luck(request):
    """随机返回6个结果,加1句毒鸡汤"""
    with open('poison-soup.txt', 'r+', encoding='utf-8') as fp:
        soup = fp.readlines()
    poison = random.choice(soup)
    luck = Music.objects.order_by('?')[:6]
    return render(request, 'music/lucky.html', {'poison': poison, 'reponse_list': luck})
    # return render(request, 'music/goodluck.html')
