OK = 0

VCODE_ERROR = 1000
LOGIN_REQUIRE = 1001
USER_NOT_EXIST = 1002
PROFILE_ERROR = 1003


class LogicError(Exception):
    code = 0

    def __str__(self):
        return self.__class__.__name__

    __repr__ = __str__



def generate_logic_error(name: str, code: int) -> LogicError:
    base_cls = (LogicError,)
    return type(name, base_cls, {'code': code})


OK = generate_logic_error('OK', 0)
VCodeError = generate_logic_error('VCodeError', 1000)
VCodeExist = generate_logic_error('VCodeExist', 1001)
LoginRequire = generate_logic_error('LoginRequire', 1002)
UserNotExist = generate_logic_error('UserNotExist', 1003)
ProfileError = generate_logic_error('ProfileError', 1004)
NotHasPerm = generate_logic_error('NotHasPerm', 1005)
