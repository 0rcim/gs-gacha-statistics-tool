import json
import sys
from common import *

if __name__=='__main__':
    if len(sys.argv) < 2: 
        print('Please specify a JSON file in UIGF format. ')
        sys.exit(1)
    gacha_types = {
        '100': R_XS, # 新手祈愿
        '200': R_CZ, # 常驻祈愿
        '301': R_UP, # 角色活动祈愿与角色活动祈愿
        '400': R_UP, # 角色活动祈愿与角色活动祈愿
        '302': R_WQ, # 武器活动祈愿
    }

    with open(sys.argv[1], 'r') as f:
        uigf_json = json.load(f)
        
        for gacha_type in gacha_types:
            table = gacha_types[gacha_type]
            table_name = table._meta.table_name
            data_list = list(map(lambda x: ({
                'uid': x['uid'],
                'gacha_type': x['gacha_type'],
                'time': x['time'],
                'name': x['name'],
                'item_type': x['item_type'],
                'rank_type': x['rank_type'],
                'id': x['id'],
            }), filter(lambda x: x['gacha_type']==gacha_type and not table.select().where((table.id==int(x['id']))).count(), uigf_json['list'])))

            if data_list:
                table.insert_many(data_list).execute()
                print(f'{table_name}\x1b[32m * 插入{len(data_list)}条记录\x1b[39m')
            else:
                print(f'{table_name} 无新纪录')