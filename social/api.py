from django.shortcuts import render

from lib.http import render_json
from social import logic



def get_rcmd_users(request):
    '''获取推荐列表'''
    page = int(request.GET.get('page', 1))  # 页码
    per_page = 10

    start = (page - 1) * per_page
    end = page + per_page
    users = logic.rcmd_users(request.user)[start:end]  # 匹配所有用户

    result = [u.to_dict() for u in users]
    return render_json(result) 


def like(request):
    '''喜欢'''
    sid = int(request.POST.get('sid'))
    is_matched = logic.like_someone(request.user, sid)
    return render_json({'is_matched': is_matched}) 


def superlike(request):
    '''超级喜欢'''
    sid = int(request.POST.get('sid'))

    return render_json(None) 


def dislike(request):
    '''不喜欢'''
    sid = int(request.POST.get('sid'))

    return render_json(None) 


def rewind(request):
    '''反悔'''
    return render_json(None) 


def show_liked_me(request):
    '''查看喜欢过我的人'''
    return render_json(None) 
