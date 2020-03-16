import random

import requests
from django.core.cache import cache

from worker import call_by_worker
from tiger import config


def gen_verify_code(length=6):
    '''产生验证码'''
    min_value = 10 ** (length - 1)
    max_value = 10 ** length
    number = random.randrange(min_value, max_value)
    return str(number)


@call_by_worker
def send_verify_code(phonenum):
    '''发送验证码'''
    vcode = gen_verify_code()
    # 为了省点短信数，这里先注释
    # params = config.HY_SMS_PARAMS.copy()
    # params['mobile'] = phonenum
    # params['content'] = params['content'] % vcode
    # response = requests.post(config.HY_SMS_URL, data=params)
    print('您的验证码是：%s。请不要把验证码泄露给其他人。' % vcode)
    cache.set('VCode-%s' % phonenum, vcode, 180)
    return None


def check_vcode(phonenum, vcode):
    '''检查验证码'''
    cached_vcode = cache.get('VCode-%s' % phonenum)
    return cached_vcode == vcode
