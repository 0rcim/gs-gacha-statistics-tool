import os
from typing import List, Literal
from peewee import *

db = SqliteDatabase(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gs-gacha-log.db'))
class R(Model):
    rid=AutoField()
    uid=IntegerField()
    gacha_type=IntegerField()
    time=DateTimeField('%Y-%m-%d %H:%M:%S')
    name=CharField()
    item_type=CharField()
    rank_type=SmallIntegerField()
    id=BigIntegerField(unique=True)
    class Meta:
        database = db

class R_XS(R):
    class Meta:
        table_name='新手池'
class R_UP(R):
    class Meta:
        table_name='UP池'
class R_CZ(R):
    class Meta:
        table_name='常驻池'
class R_WQ(R):
    class Meta:
        table_name='武器池'

class _RTyping:
    rid: int
    uid: int
    gacha_type: Literal[100, 200, 301, 302, 400]
    time: str
    name: str
    item_type: Literal['角色', '武器']
    rank_type: Literal[3, 4, 5]
    id: int

RL=List[_RTyping]

db.connect()
db.create_tables([R_XS, R_UP, R_CZ, R_WQ])

gacha_types = {
    '100': R_XS, # 新手祈愿
    '200': R_CZ, # 常驻祈愿
    '301': R_UP, # 角色活动祈愿与角色活动祈愿-2
    '302': R_WQ, # 武器活动祈愿
}

api_uri = 'https://hk4e-api-os.hoyoverse.com/gacha_info/api/getGachaLog'

cz_character_list = [
    '迪希雅',
    '提纳里',
    '刻晴',
    '莫娜',
    '七七',
    '迪卢克',
    '琴',
]