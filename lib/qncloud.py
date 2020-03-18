from urllib.parse import urljoin
from qiniu import Auth, put_file, etag

from tiger import config
from tiger import settings

from worker import call_by_worker

QN_Auth = Auth(config.QN_ACCESS_KEY, config.QN_SECRET_KEY)


def get_qn_url(filename):
    return urljoin(config.QN_BASE_URL, filename)


def upload_to_qiniu(localfile, key):
    '''将本地文件上传到七牛云

    Args:
        localfile: 本地文件位置
        key: 上传到云服务器后的文件名
    '''
    # 生成上传 Token 可以指定过期时间等
    token = QN_Auth.upload_token(config.QN_BUCKET, key, 3600)

    # 要上传文件的本地路径
    ret, info = put_file(token, key, localfile)

    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)

    url = get_qn_url(filename)
    return ret, info, url


async_upload_to_qiniu = call_by_worker(upload_to_qiniu)
