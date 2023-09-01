"""
Data source:https://data.eastmoney.com/cjsj/cpi.html
"""
import easymoney
import requests
import json
import pandas as pd

def get_data():
    params = {
        'columns': 'REPORT_DATE,NATIONAL_BASE,CITY_BASE,RURAL_BASE',
        'sortColumns': 'REPORT_DATE',
        'sortTypes': '-1',
        'source': 'WEB',
        'client': 'WEB',
        'reportName': 'RPT_ECONOMY_CPI'
    }
    print(f'begin request, url:{easymoney.base_api},params:{params}')
    response = requests.get(easymoney.base_api, params=params)
    if response.status_code == 200:
        resp = json.loads(response.text)
        store_data(resp)
    else:
        print(f'Fail to request, url:{easymoney.base_api}')


def store_data(resp, update_rows=None):
    """
    store cpi data
    :param resp:
    :param update_rows: for update, save the latest {update_rows} in list
    :return:
    """
    # get cpi list
    cpi_history_raw = resp['result']['data']
    # {"REPORT_DATE":"2023-07-01 00:00:00","NATIONAL_BASE":99.7,"CITY_BASE":99.8,"RURAL_BASE":99.4}
    # store in ../data/macro
    file_name = f'{easymoney.macro_index_file_path}cpi.h5'
    dataset = 'china'
    try:
        cpi_history = pd.read_hdf(file_name, key=dataset)
    except FileNotFoundError:
        cpi_history = pd.DataFrame(columns=['DATE', 'NATIONAL_BASE', 'CITY_BASE', 'RURAL_BASE'])
    for raw_object in cpi_history_raw:
        cpi = {'DATE': raw_object['REPORT_DATE'][:10], 'NATIONAL_BASE': raw_object['NATIONAL_BASE'],
               'CITY_BASE': raw_object['CITY_BASE'], 'RURAL_BASE': raw_object['RURAL_BASE']}
        cpi_history = pd.concat([cpi_history, pd.DataFrame(cpi, index=[0])], ignore_index=True)
    cpi_history.to_hdf(file_name, key=dataset, mode='w', format='table')
    print('stored cpi data successfully.')

def read_data():
    file_name = f'{easymoney.macro_index_file_path}cpi.h5'
    dataset = 'china'
    cpi_history = pd.read_hdf(file_name, key=dataset)
    return cpi_history

if __name__ == "__main__":
    get_data()
    # read_data()
