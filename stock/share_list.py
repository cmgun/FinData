"""
Get share list by sector
BK1037: 消费电子
"""
import requests
import json
import pandas as pd
import re
import datetime


def get_share_list(code):
    """
    param:
    f2: latest price, f3: quote change, f4: changes, f5: volume, f6: turnover,
    f7: amplitude, f8: turnover rate, f9: P/E ratio (dynamic), f10: quantity ratio,
    f12: code, f14: name, f15: highest price, f16: lowest price, f17: today's open, f18: yesterday's close, f23: P/B PBR,
    f13: 0-SZ, 1-SH
    :return: f12, f13, f14
    """
    url = 'http://22.push2.eastmoney.com/api/qt/clist/get'
    page_no = 1
    page_size = 50
    params = {
        'cb': 'jQuery112407769569993294949_1694508927728',
        'fid': 'f62',
        'pn': {page_no},  # page no
        'pz': {page_size},
        'po': 1,
        'np': 1,
        'ut': 'b2884a393a59ad64002292a3e90d46a5',
        'fltt': 2,
        'invt': 2,
        'wbp2u': '8696015110843672|0|1|0|web',
        'fs': f'b:{code}',
        'fields': 'f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13'
    }
    response = requests.get(url, params)
    result = []
    if response.status_code == 200:
        match = re.search(r'\((.*?)\)', response.text)
        content = match.group(1)
        resp = json.loads(content)
        data = resp['data']['diff']
        for info in data:
            code = {'code': info['f12'], 'sector': info['f13']}
            result.append(code)
        pages = resp['data']['total'] / page_size
        while pages > 1:
            page_no += 1
            params['pn'] = page_no
            response = requests.get(url, params)
            match = re.search(r'\((.*?)\)', response.text)
            content = match.group(1)
            resp = json.loads(content)
            data = resp['data']['diff']
            for info in data:
                code = {'code': info['f12'], 'name': info['f14'], 'sector': info['f13']}
                result.append(code)
            pages -= 1
    else:
        print(f'查询失败,url:{url}')
    return result

if __name__ == "__main__":
    codes = get_share_list('BK1037')
