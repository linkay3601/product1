from common import errors
from lib.http import render_json
from lib.sms import send_verify_code
from lib.sms import check_vcode

from user.models import User
from user.forms import ProfileForm

from user.logic import save_upload_file
from user.logic import upload_avatar_to_qn


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
        raise errors.VcodeError.code


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
        raise errors.ProfileError.code


def upload_avatar(request):
    '''上传个人形象'''
    avatar = request.FILES.get('avatar')
    filepath, filename = save_upload_file(request.user, request.user, avatar)
    # 上传个人头像到七牛云 「未测试」
    # upload_avatar_to_qn(filepath, filename)
    return render_json(None)
