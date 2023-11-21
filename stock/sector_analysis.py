"""
Query sector data analysis
"""
import requests
import json
import pandas as pd
import re
import datetime
import daily_trade_info as kline
from concurrent.futures import ThreadPoolExecutor


def get_sector_list(type):
    """
    param:
    f2: latest price, f3: %change, f4: changes, f5: volume, f6: turnover,
    f7: amplitude, f8: turnover rate, f9: P/E ratio (dynamic), f10: quantity ratio,
    f12: code, f13: sector code, f14: name, f15: highest price, f16: lowest price, f17: today's open, f18: yesterday's close,
    f20: Market Capitalization, f23: P/B PBR,
    f13: 0-SZ, 1-SH
    :return: f12, f13, f14,
    """
    url = 'https://20.push2.eastmoney.com/api/qt/clist/get'
    page_no = 1
    page_size = 20
    params = {
        'cb': 'jQuery112407529189286376934_1696915626701',
        # 'fid': 'f62',
        'fid': 'f3',
        'pn': {page_no},  # page no
        'pz': {page_size},
        'po': 1,
        'np': 1,
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': 2,
        'invt': 2,
        'wbp2u': '8696015110843672|0|1|0|web',
        'fs': f'm:90 t:{type} f:!50',
        # 'fields': 'f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222'
    }
    response = requests.get(url, params)
    result = []
    if response.status_code == 200:
        match = re.search(r'\((.*?)\)', response.text)
        content = match.group(1)
        resp = json.loads(content)
        data = resp['data']['diff']
        for info in data:
            code = {'code': info['f12'], 'name': info['f14'], 'sector': info['f13'], 'market_cap': info['f20']}
            result.append(code)
        pages = resp['data']['total'] / page_size
        # next page
        while pages > 1:
            page_no += 1
            params['pn'] = page_no
            response = requests.get(url, params)
            match = re.search(r'\((.*)\);', response.text)
            content = match.group(1)
            resp = json.loads(content)
            data = resp['data']['diff']
            for info in data:
                code = {'code': info['f12'], 'name': info['f14'], 'sector': info['f13'], 'market_cap': info['f20']}
                result.append(code)
            pages -= 1
    else:
        print(f'查询失败,url:{url}')
    return result

def save_sector_his(sector_codes):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(save_data, sector_data['sector'], sector_data['code']) for sector_data in sector_codes]


def save_data(sector, code):
    print(f'Query data:{code}')
    history = kline.getDailyTrade(code, sector)
    df = pd.DataFrame(columns=['date', 'open', 'close', 'highest', 'lowest', 'volume', 'turnover', 'amplitude',
                               '%change', 'turnover change', 'turnover rate'])
    for info_str in history:
        info = info_str.split(',')
        data = {'date': info[0], 'open': info[1], 'close': info[2], 'highest': info[3],
                'lowest': info[4], 'volume': info[5], 'turnover': info[6], 'amplitude': info[7],
                '%change': info[8], 'turnover change': info[8], 'turnover rate': info[9]}
        df = pd.concat([df, pd.DataFrame(data, index=[0])], ignore_index=True)
    file_name = f'../data/stock/sector/{code}.csv'
    df.to_csv(file_name)
    print(f'stored {file_name} successfully.')

def calculate_change(sector_codes):
    current_date = datetime.datetime.now()
    end_date = current_date.strftime('%Y-%m-%d')
    output_df = pd.DataFrame(
        columns=['code', 'name', 'start_date', 'start_price', 'end_date', 'end_price', 'change'])
    for sector_data in sector_codes:
        # from_date = current_date.replace(year=current_date.year - 2)
        from_date = datetime.date(2021, 3, 1)
        print(f'from date:{from_date}')
        start_date = from_date.strftime('%Y-%m-%d')
        code = sector_data['code']
        file_name = f'../data/stock/sector/{code}.csv'
        df = pd.read_csv(file_name, dtype={'date': str})
        start = df[df['date'] == start_date]
        if start.empty:
            start = df.iloc[0]
            start_date = start['date']
            start_price = start['close']
        else:
            start_price = start['close'].iloc[0]
        end = df[df['date'] == end_date]
        end_price = end['close'].iloc[0]
        change = ((end_price - start_price) / start_price) * 100
        data = {'code': code, 'name': sector_data['name'], 'market_cap': sector_data['market_cap']/100000000,
                'start_date': start_date, 'start_price': start_price,
                'end_date': end_date, 'end_price': end_price, 'change': change}
        output_df = pd.concat([output_df, pd.DataFrame(data, index=[0])], ignore_index=True)
        print(f'{code} calculation finished.')
    output_file_name = f'../data/stock/sector/change.csv'
    output_df.to_csv(output_file_name)



if __name__ == "__main__":
    # 2:industry 3:concept
    sector_codes = get_sector_list(2)
    save_sector_his(sector_codes)
    calculate_change(sector_codes)




