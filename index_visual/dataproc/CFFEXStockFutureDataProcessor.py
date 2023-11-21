"""
CFFEX股指期货历史数据处理
取今结算作为交割价格
"""
import pandas as pd
import os
import chardet
import re

month = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'
]
filepath = '../../data/CFFEX/'

def saveHistoryData(start, end, product_code):
    """
    从历史记录里提取每天交易数据：今结算
    :param start: 开始年份
    :param end: 结束年份
    :return:
    """
    dates, prices1, prices2, prices3, prices4 = getHistoryPrice(start, end, product_code)
    result = pd.DataFrame({'date': dates, '当月今结算': prices1, '隔月今结算': prices2, '当季今结算': prices3, '隔季今结算': prices4})
    result.to_csv(f'../data/backtrack/{product_code}HistoryData.csv', index=False)

def addHistoryData(year, month, product_code):
    dates, prices1, prices2, prices3, prices4 = getHistoryPriceByMonth(year, month, product_code)
    result = pd.DataFrame({'date': dates, '当月今结算': prices1, '隔月今结算': prices2, '当季今结算': prices3, '隔季今结算': prices4})
    filepath = f'../data/backtrack/{product_code}HistoryData.csv'
    history = pd.read_csv(filepath)
    updated_df = pd.concat([history, result], ignore_index=True)
    updated_df.to_csv(filepath, index=False)

def getHistoryPrice(start, end, product_code):
    """
    四种合约的历史价格获取，价格取【今结算】
    :param start:
    :param end:
    :param product_code:
    :return: 日期列表，当月价格列表，隔月，当季，隔季
    """
    current_y = int(start)
    end_y = int(end)
    dates = []
    prices1 = []
    prices2 = []
    prices3 = []
    prices4 = []
    while current_y <= end_y:
        for MM in month:
            yyyyMM = str(current_y) + MM
            # 循环获取文件
            dir = filepath + yyyyMM
            if not os.path.exists(dir):
                break
            for filename in os.listdir(dir):
                file_path = dir + '/' + filename
                if os.path.isfile(file_path):
                    print(f'当前处理：{file_path}')
                    date, price1, price2, price3, price4 = getPrice(product_code, file_path)
                    dates.append(date)
                    prices1.append(price1)
                    prices2.append(price2)
                    prices3.append(price3)
                    prices4.append(price4)
                    print(f'处理结束：{file_path}')
        current_y += 1
    return dates, prices1, prices2, prices3, prices4

def getHistoryPriceByMonth(year, MM, product_code):
    """
    四种合约的历史价格获取，价格取【今结算】
    :param start:
    :param end:
    :param product_code:
    :return: 日期列表，当月价格列表，隔月，当季，隔季
    """
    dates = []
    prices1 = []
    prices2 = []
    prices3 = []
    prices4 = []
    # 循环获取文件
    dir = filepath + year + MM
    for filename in os.listdir(dir):
        file_path = dir + '/' + filename
        if os.path.isfile(file_path):
            print(f'当前处理：{file_path}')
            date, price1, price2, price3, price4 = getPrice(product_code, file_path)
            dates.append(date)
            prices1.append(price1)
            prices2.append(price2)
            prices3.append(price3)
            prices4.append(price4)
            print(f'处理结束：{file_path}')
    return dates, prices1, prices2, prices3, prices4


def getPrice(product_code, filepath):
    """
    获取每日股指期货的4类合同结算价
    :param filepath:
    :param product_code: 产品代号，IC，IM
    :return: 日期，当月，隔月，当季，隔季
    """
    with open(filepath, 'rb') as f:
        file_encoding = chardet.detect(f.read())['encoding']
    data = pd.read_csv(filepath, encoding=file_encoding)
    date_regex = r"/(\d{8})_"
    match = re.search(date_regex, filepath)
    date = match.group(1)
    target_attr = '今结算'
    # 当月
    price1 = data.loc[data.合约代码.str.contains(product_code, case=False)].iloc[0][target_attr]
    # 隔月
    price2 = data.loc[data.合约代码.str.contains(product_code, case=False)].iloc[1][target_attr]
    # 当季
    price3 = data.loc[data.合约代码.str.contains(product_code, case=False)].iloc[2][target_attr]
    # 隔季
    price4 = data.loc[data.合约代码.str.contains(product_code, case=False)].iloc[3][target_attr]
    return date, price1, price2, price3, price4

if __name__ == "__main__":
    code_mapping = {'IM': '000852', 'IC': '000905'}
    product_code = 'IC'
    # 首次获取历史数据
    # start = '2016'
    # end = '2023'
    # saveHistoryData(start, end, product_code)
    # 后续进行增量数据添加
    addHistoryData('2015', '12', product_code)
