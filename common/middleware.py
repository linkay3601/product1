import logging

from django.utils.deprecation import MiddlewareMixin

from common import errors
from lib.http import render_json
from user.models import User

err_logger = logging.getLogger('err')


class AutoMiddleware(MiddlewareMixin):
    white_list = [
        '/api/user/vcode',
        '/api/user/login',
    ]

    def process_request(self, request):
        # 检查当前 path 是否在白名单内
        if request.path in self.white_list:
            return

        # 用户登录验证
        uid = request.session.get('uid')
        if uid is None:
            raise errors.LoginRequire
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            raise errors.UserNotExist
        else:
            # 将 user 对象添加到 request
            request.user = user


class LogicErrorMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, errors.LogicError):
            err_logger.error(f'LogicError: {exception}')
            return render_json(None, exception.code)  # 处理逻辑错误
