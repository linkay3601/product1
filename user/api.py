from common import errors
from lib.http import render_json
from lib.sms import send_verify_code
from lib.sms import check_vcode

from user.models import User
from user.forms import ProfileForm


def get_verify_code(request):
    '''短信发送'''
    phonenum = request.GET.get('phonenum')
    send_verify_code(phonenum)
    return render_json(None)


def login(request):
    '''注册、登录'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    if check_vcode(phonenum, vcode):
        user, created = User.objects.get_or_create(phonenum=phonenum)
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        return render_json(None, errors.VCODE_ERROR)


def show_profile(request):
    '''查看个人资料'''
    user = request.user
    return render_json(user.profile.to_dict())


def modify_profile(request):
    '''修改个人资料'''
    form = ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.id = request.user.id
        profile.save()
        return render_json(profile.to_dict())
    else:
        return render_json(form.errors, errors.PROFILE_ERROR)


def upload_avatar(request):
    return render()


