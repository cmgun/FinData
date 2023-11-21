"""
CFFEX股指期货策略集
strategy1: 当月连续永存
"""
import pandas as pd
from tools import DateTool
import datetime

month = [
    '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'
]
seasons = [
    '03', '06', '09', '12'
]
half_years = [
    '06', '12'
]
filepath = '../data/backtrack/'

def strategy1(product_code):
    '''
    当月连续永存
    sell:当月交割日，buy:当月交割日{+1}
    :param product_code:
    :return: 输出{product_code}strategy1.csv
    '''
    history = pd.read_csv(f'{filepath}{product_code}HistoryData.csv', dtype={'date': str})
    raw1 = history.iloc[0]
    date = raw1.date
    # year = int(date[:4])
    year = 2016
    end_year = 2023
    # 结果输出内容
    result_date = []
    # 结算日卖，下一个工作日买，当月连续永存
    delta1_param1 = []
    delta1_param2 = []
    delta1_param1_date = []
    delta1_param2_date = []
    delta1 = []
    while year <= end_year:
        for MM in month:
            # 交割日
            settle_date_raw = DateTool.get_target_day(year, MM, 4, 3)
            settle_date = settle_date_raw.strftime('%Y%m%d')
            settle_day = history.loc[history.date == settle_date]
            if len(settle_day) <= 0:
                continue
            # sell
            sell_price = settle_day.iloc[0]['当月今结算']
            # 结算日前一日
            settle_date_raw1 = settle_date_raw + datetime.timedelta(days=-1)
            settle_date1 = settle_date_raw1.strftime('%Y%m%d')
            settle_day1 = history.loc[history.date == settle_date1]
            # buy
            buyer_date_raw = settle_date_raw + datetime.timedelta(days=1)
            buyer_date_raw = DateTool.get_closest_workday(buyer_date_raw.year, buyer_date_raw.month, buyer_date_raw.day)
            buyer_date = buyer_date_raw.strftime('%Y%m%d')
            buyer_day = history.loc[history.date == buyer_date]
            if len(buyer_day) <= 0:
                continue
            buy_price = buyer_day.iloc[0]['当月今结算']
            delta1_param2.append(buy_price)
            delta1_param1.append(sell_price)
            delta1_param1_date.append(settle_date)
            delta1_param2_date.append(buyer_date)
            delta = sell_price - buy_price
            delta1.append(delta)
            result_date.append(str(year) + MM)
        year += 1
    result = pd.DataFrame({'date': result_date,
                           '日期1': delta1_param1_date, '当月连续永存（结算日价格）': delta1_param1,
                           '日期2': delta1_param2_date, '当月连续永存（结算日下一日价格）': delta1_param2, '当月连续永存（结算日价格-下一个工作日价格）': delta1})
    result.loc[len(result.index)] = ['sum', '', '', '', '',sum(delta1)]
    result.to_csv(f'../data/backtrack/{product_code}strategy1.csv', index=False)

def strategy2(product_code):
    '''
    隔月连续
    sell:当月交割日，buy:当月交割日{+1}
    :param product_code:
    :return: 输出{product_code}strategy1.csv
    '''
    history = pd.read_csv(f'{filepath}{product_code}HistoryData.csv', dtype={'date': str})
    raw1 = history.iloc[0]
    date = raw1.date
    # year = int(date[:4])
    year = 2016
    end_year = 2023
    # 结果输出内容
    result_date = []
    # 结算日卖，下一个工作日买，当月连续永存
    delta1_param1 = []
    delta1_param2 = []
    delta1_param1_date = []
    delta1_param2_date = []
    delta1 = []
    while year <= end_year:
        for MM in month:
            # 交割日
            settle_date_raw = DateTool.get_target_day(year, MM, 4, 3)
            settle_date = settle_date_raw.strftime('%Y%m%d')
            settle_day = history.loc[history.date == settle_date]
            if len(settle_day) <= 0:
                continue
            # sell
            sell_price = settle_day.iloc[0]['隔月今结算']
            # 结算日前一日
            settle_date_raw1 = settle_date_raw + datetime.timedelta(days=-1)
            settle_date1 = settle_date_raw1.strftime('%Y%m%d')
            settle_day1 = history.loc[history.date == settle_date1]
            # buy
            buyer_date_raw = settle_date_raw + datetime.timedelta(days=1)
            buyer_date_raw = DateTool.get_closest_workday(buyer_date_raw.year, buyer_date_raw.month, buyer_date_raw.day)
            buyer_date = buyer_date_raw.strftime('%Y%m%d')
            buyer_day = history.loc[history.date == buyer_date]
            if len(buyer_day) <= 0:
                continue
            buy_price = buyer_day.iloc[0]['隔月今结算']
            delta1_param2.append(buy_price)
            delta1_param1.append(sell_price)
            delta1_param1_date.append(settle_date)
            delta1_param2_date.append(buyer_date)
            delta = sell_price - buy_price
            delta1.append(delta)
            result_date.append(str(year) + MM)
        year += 1
    result = pd.DataFrame({'date': result_date,
                           '日期1': delta1_param1_date, '隔月连续永存（结算日价格）': delta1_param1,
                           '日期2': delta1_param2_date, '隔月连续永存（结算日下一日价格）': delta1_param2, '隔月连续永存（结算日价格-下一个工作日价格）': delta1})
    result.loc[len(result.index)] = ['sum', '', '', '', '',sum(delta1)]
    result.to_csv(f'../data/backtrack/{product_code}strategy2.csv', index=False)

def strategy3(product_code):
    '''
    当月切当季
    sell:当季交割日，buy:当季交割日{+1}
    :param product_code:
    :return: 输出{product_code}strategy1.csv
    '''
    history = pd.read_csv(f'{filepath}{product_code}HistoryData.csv', dtype={'date': str})
    raw1 = history.iloc[0]
    date = raw1.date
    # year = int(date[:4])
    year = 2015
    end_year = 2023
    # 结果输出内容
    result_date = []
    # 结算日卖，下一个工作日买，当月连续永存
    delta1_param1 = []
    delta1_param2 = []
    delta1_param1_date = []
    delta1_param2_date = []
    delta1 = []
    while year <= end_year:
        for MM in seasons:
            # 交割日
            settle_date_raw = DateTool.get_target_day(year, MM, 4, 3)
            settle_date_raw = DateTool.get_closest_workday(settle_date_raw.year, settle_date_raw.month, settle_date_raw.day)
            settle_date = settle_date_raw.strftime('%Y%m%d')
            settle_day = history.loc[history.date == settle_date]
            if len(settle_day) <= 0:
                continue
            # sell
            sell_price = settle_day.iloc[0]['当月今结算']
            # buy
            buyer_date_raw = settle_date_raw + datetime.timedelta(days=1)
            buyer_date_raw = DateTool.get_closest_workday(buyer_date_raw.year, buyer_date_raw.month, buyer_date_raw.day)
            buyer_date = buyer_date_raw.strftime('%Y%m%d')
            buyer_day = history.loc[history.date == buyer_date]
            if len(buyer_day) <= 0:
                continue
            buy_price = buyer_day.iloc[0]['当季今结算']
            delta1_param2.append(buy_price)
            delta1_param1.append(sell_price)
            delta1_param1_date.append(settle_date)
            delta1_param2_date.append(buyer_date)
            delta = sell_price - buy_price
            delta1.append(delta)
            result_date.append(str(year) + MM)
        year += 1
    result = pd.DataFrame({'date': result_date,
                           '日期1': delta1_param1_date, '当月连续永存（结算日价格）': delta1_param1,
                           '日期2': delta1_param2_date, '当季连续永存（结算日下一日价格）': delta1_param2, '当季连续永存（结算日价格-下一个工作日价格）': delta1})
    result.loc[len(result.index)] = ['sum', '', '', '', '',sum(delta1)]
    result.to_csv(f'../data/backtrack/{product_code}strategy3.csv', index=False)

def strategy4(product_code):
    '''
    当月切隔季
    sell:当季交割日，buy:当季交割日{+1}
    :param product_code:
    :return: 输出{product_code}strategy1.csv
    '''
    history = pd.read_csv(f'{filepath}{product_code}HistoryData.csv', dtype={'date': str})
    raw1 = history.iloc[0]
    date = raw1.date
    # year = int(date[:4])
    year = 2015
    end_year = 2023
    # 结果输出内容
    result_date = []
    # 结算日卖，下一个工作日买，当月连续永存
    delta1_param1 = []
    delta1_param2 = []
    delta1_param1_date = []
    delta1_param2_date = []
    delta1 = []
    while year <= end_year:
        for MM in half_years:
            # 交割日
            settle_date_raw = DateTool.get_target_day(year, MM, 4, 3)
            settle_date_raw = DateTool.get_closest_workday(settle_date_raw.year, settle_date_raw.month, settle_date_raw.day)
            settle_date = settle_date_raw.strftime('%Y%m%d')
            settle_day = history.loc[history.date == settle_date]
            if len(settle_day) <= 0:
                continue
            # sell
            sell_price = settle_day.iloc[0]['当月今结算']
            # buy
            buyer_date_raw = settle_date_raw + datetime.timedelta(days=1)
            buyer_date_raw = DateTool.get_closest_workday(buyer_date_raw.year, buyer_date_raw.month, buyer_date_raw.day)
            buyer_date = buyer_date_raw.strftime('%Y%m%d')
            buyer_day = history.loc[history.date == buyer_date]
            if len(buyer_day) <= 0:
                continue
            buy_price = buyer_day.iloc[0]['隔季今结算']
            delta1_param2.append(buy_price)
            delta1_param1.append(sell_price)
            delta1_param1_date.append(settle_date)
            delta1_param2_date.append(buyer_date)
            delta = sell_price - buy_price
            delta1.append(delta)
            result_date.append(str(year) + MM)
        year += 1
    result = pd.DataFrame({'date': result_date,
                           '日期1': delta1_param1_date, '当月连续永存（结算日价格）': delta1_param1,
                           '日期2': delta1_param2_date, '隔季连续永存（结算日下一日价格）': delta1_param2, '隔季连续永存（结算日价格-下一个工作日价格）': delta1})
    result.loc[len(result.index)] = ['sum', '', '', '', '',sum(delta1)]
    result.to_csv(f'../data/backtrack/{product_code}strategy4.csv', index=False)


if __name__ == "__main__":
    code_mapping = {'IM': '000852', 'IC': '000905'}
    strategy4('IC')
