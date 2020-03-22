import datetime

from user.models import User

from social.models import Swiped
from social.models import Friend


def rcmd_users(user):
    dating_sex = user.profile.dating_sex
    location = user.profile.location
    min_dating_age = user.profile.min_dating_age
    max_dating_age = user.profile.max_dating_age

    curr_year = datetime.date.today().year
    min_year = curr_year - max_dating_age
    max_year = curr_year - min_dating_age
    users = User.objects.filter(sex=dating_sex,
                                location=location,
                                birth_year__gte=min_year,
                                birth_year__lte=max_year)
    return users


def like_someone(user, sid):
    Swiped.like(user.id, sid)
    if Swiped.is_liked(sid, user.id):  # 检查对方是否喜欢过自己
        Friend.make_friends(uid1=user.id, uid2=sid)
        return True
    else:
        return False
    return users


def superlike_someone(user, sid):
    Swiped.superlike(user.id, sid)
    if Swiped.is_liked(sid, user.id):  # 检查对方是否喜欢过自己
        Friend.make_friends(uid1=user.id, uid2=sid)
        return True
    else:
        return False


def rewind(user):
    '''反悔'''
    # 取出最后一次滑动记录
    swiped = Swiped.objects.filter(uid=user.id).latest()

    # 删除好友关系
    if swiped.flag in ['superlike', 'like']:
        Friend.break_off(user.id, swiped.sid)

    # 删除滑动记录
    swiped.delete()


def users_liked_me(user):
    swipeds = Swiped.like_me(user.id)
    swiped_uid_list = [s.uid for s in swipeds]
    return User.objects.filter(id__in=swiped_uid_list)
