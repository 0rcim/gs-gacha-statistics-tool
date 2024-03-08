import json
from urllib import parse, request
from utils.common import *

def run(page_url: str):
    n_count = 0
    q = parse.parse_qs(parse.urlparse(page_url).query)

    q = {k: q[k][0] for k in q}

    ext_query_param = {
        'gacha_type': '0',
        'page': '0',
        'size': '20',
        'end_id': '0'
    }

    for gacha_type in gacha_types:
        table = gacha_types[gacha_type]
        table_name = table._meta.table_name
        print()
        print(f'\x1b[34m### {table_name}\x1b[39m')
        _json=[]
        end_id='0'
        page=0
        while True:
            page+=1
            ext_query_param['page'] = page
            ext_query_param['gacha_type'] = gacha_type
            reqname = f'{gacha_type}-{page}'
            print(f'\x1b[32m{reqname}\x1b[39m')
            # print(f'{table_name}-{page} end_id: {end_id}')
            if _json and _json['data'] and _json['data']['list']:
                end_id = _json['data']['list'][-1]['id']
            ext_query_param['end_id'] = end_id
            # print(f'{table_name}-{page} end_id: {end_id}')
            query_str = parse.urlencode({**q, **ext_query_param})
            r = request.urlopen(request.Request(api_uri+f'?{query_str}', method='GET')).read()
            _json = json.loads(r)
            # print('Got data: ', {'api_url': api_uri+f'?{query_str}', 'json': _json})
            if _json:
                if _json['data'] and _json['data']['list']:
                    _list = _json['data']['list']
                    data_list = list(map(lambda x: ({
                        'uid': x['uid'],
                        'gacha_type': x['gacha_type'],
                        'time': x['time'],
                        'name': x['name'],
                        'item_type': x['item_type'],
                        'rank_type': x['rank_type'],
                        'id': x['id'],
                    }), filter(lambda x: not table.select().where(table.id==int(x['id'])).count(), _list)))
                    
                    if data_list:
                        n_count += len(data_list)
                        table.insert_many(data_list).execute()
                        print(f'{table_name}\x1b[32m * 插入{len(data_list)}条记录\x1b[39m')
                    else:
                        print(f'{table_name} 无新纪录')
                    continue
            print(f'{table_name} [{page}]: Empty data: {_json}')
            break
    return n_count
