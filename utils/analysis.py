import datetime
from typing import Dict
from utils.common import *

TOTAL_COUNT=0

def print_total_count(summary_dict: Dict={}):
    total_new_record_count = summary_dict.get('total_new', 0)
    print(f'    总计：{TOTAL_COUNT}抽', end='')
    if total_new_record_count:
        print(f'\x1b[32m(+{total_new_record_count})\x1b[39m', end='')
    print()

def print_time():
    print('统计时间：%s' % datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d %H:%M:%S'))

def time_range(ordre_list: RL):
    if len(ordre_list)<=0: return ''
    return f"[\x1b[32m{ordre_list[-1].time}\x1b[39m ~ \x1b[32m{ordre_list[0].time}\x1b[39m]"

def _5_stars_analysis(order_list: RL):
    if len(order_list)<=0: return []
    _tmp_count=0
    _5_=[]
    for item in order_list:
        if item.rank_type==5:
            _5_.append({'item': item, 'count': int(_tmp_count), 'is_cz': item.name in cz_character_list})
            _tmp_count=0
        _tmp_count+=1
    _5_.append({'item': item, 'count': int(_tmp_count), 'is_cz': item.name in cz_character_list})
    _5_.reverse()
    return _5_

def _4_star_analysis(order_list: RL):
    _tmp_count=0
    _4_already=0
    _list = order_list.copy()
    _list.reverse()
    for item in _list:
        if item.rank_type==4:
            _4_already=int(_tmp_count)
            break 
        _tmp_count+=1
    return {'_4_already': _4_already}
def analysis():
    global TOTAL_COUNT
    for gacha_type in gacha_types:
        table = gacha_types[gacha_type]
        table_name = table._meta.table_name
        _list: RL = list(table.select().order_by(table.time.asc()).namedtuples())
        TOTAL_COUNT += len(_list)
        print()
        print(f'\033[1m### {table_name}(\x1b[32m{len(_list)}\x1b[39m){time_range(_list)}\033[0m')
        _5_ = _5_stars_analysis(_list)
        _5_average = '%.2f' % (sum(map(lambda x: x['count'], _5_))/len(_5_)) if _5_ else 0
        _5_already = _5_[0]['count'] if _5_ else 0
        _5_percent = '%.2f' % (len(_5_[1:])/len(_list)*100) if _5_ else 0
        _4_percent = '%.2f' % (len(list(filter(lambda x: x.rank_type==4, _list)))/len(_list)*100) if _list else 0
        _3_percent = '%.2f' % (len(list(filter(lambda x: x.rank_type==3, _list)))/len(_list)*100) if _list else 0
        _5_listing = f'---\n'+(
            '\n'.join(map(
            lambda x: 
                f"{x['item'].time}\x1b[{39 if x['is_cz'] else 33}m[{x['count']}] {x['item'].name}\x1b[39m", _5_[1:]
            ))
        ) if _5_ else ''

        _4_ = _4_star_analysis(_list)
        print(f"""\x1b[33m[五星：{_5_percent}%]\x1b[36m
\x1b[34m[四星：{_4_percent}%]\x1b[39m
\x1b[36m[三星：{_3_percent}%]\x1b[39m
---
平均{_5_average}抽一个五星
已累计\x1b[36m {_5_already} \x1b[39m抽未出五星
已累计\x1b[36m  {_4_['_4_already']} \x1b[39m抽未出四星
{_5_listing}
""")

if __name__=='__main__':
    pass