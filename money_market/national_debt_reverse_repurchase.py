"""
Data source:https://hqdata.compass.cn/
Missing 2020,2021
"""
import requests
import json
import pandas as pd
import re

def get_data(code):
    url1 = f'https://hqdata.compass.cn/test/kline.py/data.znzDo?cmd={code}|2012,2013,2014,2015,2016|0.22469521583574648&crossdomain=1693830862996509'
    url2 = f'https://hqdata.compass.cn/test/kline.py/data.znzDo?cmd={code}|2017,2018,2019,2020,2021,2022,2023,|0.22469521583574648&crossdomain=1693830862996509'
    print(f'begin request, url:{url1}')
    response1 = requests.get(url1)
    if response1.status_code == 200:
        matche = re.search(r'"(.*?)"\);0', response1.text)
        if matche:
            print(matche.group(1))
            result = matche.group(1)
            result = result.replace('\\', '')
            resp1 = json.loads(result)
            store_data(resp1, code)
    else:
        print(f'Fail to request, url:{url1}')
    print(f'begin request, url:{url2}')
    response2 = requests.get(url2)
    if response2.status_code == 200:
        matche = re.search(r'"(.*?)"\);0', response2.text)
        if matche:
            print(matche.group(1))
            result = matche.group(1)
            result = result.replace('\\', '')
            resp2 = json.loads(result)
            store_data(resp2, code)
    else:
        print(f'Fail to request, url:{url2}')


def store_data(resp, code, update_rows=None):
    file_name = f'../data/money_market/ndrr{code}.h5'
    dataset = code
    try:
        ndrr_history = pd.read_hdf(file_name, key=dataset)
    except FileNotFoundError:
        ndrr_history = pd.DataFrame(columns=['DATE', 'START', 'HIGH', 'LOW', 'CLOSE', 'QUANTITY', 'AMOUNT'])
    except KeyError:
        ndrr_history = pd.read_hdf(file_name)
        ndrr_history.to_hdf(file_name, key=dataset, mode='w')
    for year_history in resp:
        history = json.loads(year_history[1])
        for day in history:
            # 日期，开，高，低，收，量，金额
            data = {'DATE': day[0], 'START': day[1], 'HIGH': day[2], 'LOW': day[3], 'CLOSE': day[4],
                    'QUANTITY': day[5], 'AMOUNT': day[6]}
            ndrr_history = pd.concat([ndrr_history, pd.DataFrame(data, index=[0])], ignore_index=True)
    ndrr_history.to_hdf(file_name, key=dataset, mode='w')
    print(f'stored ndrr {code} successfully.')

# def read_data():
#     file_name = f'{easymoney.macro_index_file_path}cpi.h5'
#     dataset = 'china'
#     cpi_history = pd.read_hdf(file_name, key=dataset)
#     return cpi_history

if __name__ == "__main__":
    code_list = [
        'SZHQ131810',
        'SZHQ131811',
        'SZHQ131800',
        'SZHQ131809',
        'SZHQ131801',
        'SZHQ131802',
        'SHHQ204001',
        'SHHQ204002',
        'SHHQ204003',
        'SHHQ204004',
        'SHHQ204007',
        'SHHQ204014',
    ]
    for code in code_list:
        get_data(code)
    # read_data()
