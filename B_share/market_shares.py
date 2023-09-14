"""
Query b-share's information from: http://quote.eastmoney.com/center/gridlist.html#b_board
"""
import requests
import json
import pandas as pd
import re
import datetime


def get_share_list():
    """
    param:
    f2: latest price, f3: quote change, f4: changes, f5: volume, f6: turnover,
    f7: amplitude, f8: turnover rate, f9: P/E ratio (dynamic), f10: quantity ratio,
    f12: code, f14: name, f15: highest price, f16: lowest price, f17: today's open, f18: yesterday's close, f23: P/B PBR
    :return:
    """
    url = 'http://22.push2.eastmoney.com/api/qt/clist/get'
    page_no = 1
    params = {
        'cb': 'jQuery112407769569993294949_1694508927728',
        'pn': {page_no},  # page no
        'pz': 200,
        'po': 1,
        'np': 1,
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': 2,
        'invt': 2,
        'wbp2u': '8696015110843672|0|1|0|web',
        'fid': 'f6',
        'fs': 'm:0+t:7,m:1+t:3',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152'
    }
    response = requests.get(url, params)
    if response.status_code == 200:
        match = re.search(r'\((.*?)\)', response.text)
        content = match.group(1)
        resp = json.loads(content)
        return resp['data']['diff']
    else:
        print(f'查询失败,url:{url}')
    return []

def store_data(share_list):
    date = datetime.date.today()
    formatted_date = date.strftime('%Y-%m-%d')
    file_name = f'../data/b_share/all_shares_{formatted_date}.csv'
    df = pd.DataFrame(columns=['CODE', 'NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'AMOUNT', 'PE', 'PB'])
    for info in share_list:
        data = {'CODE': info['f12'], 'NAME': info['f14'] , 'OPEN': info['f17'], 'HIGH': info['f15'],
                'LOW': info['f16'], 'CLOSE': info['f2'], 'AMOUNT': info['f6'], 'PE': info['f9'], 'PB': info['f23']}
        df = pd.concat([df, pd.DataFrame(data, index=[0])], ignore_index=True)
    df.to_csv(file_name)
    print(f'stored {file_name} successfully.')

if __name__ == "__main__":
    share_list = get_share_list()
    store_data(share_list)
