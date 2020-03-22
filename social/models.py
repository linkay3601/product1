from django.db import models


class Swiped(models.Model):
    '''滑动记录'''
    FALGS = (
        ('superlike', '上滑'),
        ('like', '右滑'),
        ('dislike', '左滑'),

    )
    uid = models.IntegerField(verbose_name='滑动者的 UID')
    sid = models.IntegerField(verbose_name='被滑动者的 UID')
    flag = models.CharField(max_length=10, choices=FALGS)
    dtime = models.DateTimeField(auto_now=True)

    @classmethod    
    def superlike(cls, uid, sid):
        obj = cls.objects.create(uid=uid, sid=sid, flag='superlike')
        return obj

    @classmethod        
    def like(cls, uid, sid):
        obj = cls.objects.create(uid=uid, sid=sid, flag='like')
        return obj

    @classmethod        
    def dislike(cls, uid, sid):
        obj = cls.objects.create(uid=uid, sid=sid, flag='dislike')
        return obj

    @classmethod
    def is_liked(cls, uid, sid):
        return cls.objects.filter(uid=uid, sid=sid, 
                                  flag__in=['superlike', 'like']).exists()


class Friend(models.Model):
    '''好友关系'''
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls, uid1, uid2):
        uid1, uid2 = sorted([uid1, uid2])
        cls.objects.get_or_create(uid1=uid1, uid2=uid2)
