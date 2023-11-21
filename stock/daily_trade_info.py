"""
Daily trade information
"""
import requests
import json
import re
import pandas as pd

def getDailyTrade(code, sector):
    """
    return daily trade information, seperated by ','
    [date, open, close, highest, lowest, volume, turnover, amplitude, %change, turnover change, turnover rate]

    :param code:
    :return:
    """
    url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get'
    params = {
        'cb': 'jQuery351005358392898952258_1689431169006',
        'secid': f'{sector}.{code}',
        'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
        'fields1': 'f1,f2,f3,f4,f5,f6',
        'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
        'klt': '101',
        'fqt': '1',
        'end': '20500101',
        'lmt': '1000000000'
    }
    # url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery351005358392898952258_1689431169006&secid=1.000905&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61&klt=101&fqt=1&end=20500101&lmt=120'
    response = requests.get(url, params)
    if response.status_code == 200:
        match = re.search(r'\((.*?)\)', response.text)
        content = match.group(1)
        resp = json.loads(content)
        return resp['data']['klines']
    else:
        print(f'查询失败,url:{url}')
    return []


def saveDailyTradeInfo(code, sector):
    history = getDailyTrade(code, sector)
    df = pd.DataFrame(columns=['date', 'open', 'close', 'highest', 'lowest', 'volume', 'turnover', 'amplitude',
                               '%change', 'turnover change', 'turnover rate'])
    for info_str in history:
        info = info_str.split(',')
        data = {'date': info[0], 'open': info[1], 'close': info[2], 'highest': info[3],
                'lowest': info[4], 'volume': info[5], 'turnover': info[6], 'amplitude': info[7],
                '%change': info[8], 'turnover change': info[8], 'turnover rate': info[9]}
        df = pd.concat([df, pd.DataFrame(data, index=[0])], ignore_index=True)
    file_name = f'../data/stock/daily/{code}.csv'
    df.to_csv(file_name)
    print(f'stored {file_name} successfully.')

if __name__ == "__main__":
    klines = getDailyTrade('600745', 'BK1037')
    print(klines)