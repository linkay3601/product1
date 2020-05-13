from django.core.cache import cache

from lib.http import render_json
from vip.models import Vip


def show_vip_permissions(request):
    key = 'VipPermissions'
    vip_permissions = cache.get(key, [])
    print(f'get from cache: {vip_permissions')

    if not vip_permissions:
        for vip in Vip.objects.filter(level__gte=1):
            vip_info = vip.to_dict()
            perm_info = []
            for perm in vip.permissions():
                perm_info.append(perm.to_dict())
            vip_info['perm_info'] = perm_info
            vip_permissions.append(vip_info)
        print(f'get from db: {vip_permissions}')
        cache.set(key, vip_permissions)
        print('set to cache')

    return render_json(vip_permissions)
