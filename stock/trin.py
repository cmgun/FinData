"""
(Emotional Index) Get current TRIN index
TRIN = (declined_amount / declined_count) / (advanced_amount / advanced_count)
"""
import stock_list
import datetime
import pandas as pd
import daily_trade_info
import concurrent.futures

'''
sector:
BK0500-HS300
'''
code = 'BK0500'

code_mapping = {
    'BK0500': 'HS300'
}

def saveStockList():
    # get stock list
    stocks = stock_list.get_stock_list(code)
    # save code list
    df = pd.DataFrame(columns=['code', 'sector'])
    for stock in stocks:
        data = {'code': str(stock['code']), 'sector': stock['sector']}
        df = pd.concat([df, pd.DataFrame(data, index=[0])], ignore_index=True)
    df['code'] = df['code'].astype(str)
    file_name = f'../data/stock/sector_stocklist_{code_mapping[code]}.csv'
    df.to_csv(file_name)
    print(f'stored {file_name} successfully.')

def currentTRINIndex():
    stocks = stock_list.get_stock_list(code)
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    declined_amt = 0
    advanced_amt = 0
    declined_cnt = 0
    advanced_cnt = 0
    for stock in stocks:
        if stock['%change'] > 0:
            advanced_cnt += 1
            advanced_amt += stock['turnover']
            # advanced_amt += stock['volume']
        elif stock['%change'] < 0:
            declined_cnt += 1
            declined_amt += stock['turnover']
            # declined_amt += stock['volume']
    trin = (declined_amt / declined_cnt) / (advanced_amt / advanced_cnt)
    print(f'time: {formatted_time}, TRIN: {trin}')


def historyTRINIndex_1():
    """
    save daily trade info
    :return:
    """
    file_name = f'../data/stock/sector_stocklist_{code_mapping[code]}.csv'
    df = pd.read_csv(file_name, dtype={'code': str})
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        task_list = []
        for index, row in df.iterrows():
            daily_trade_info.saveDailyTradeInfo(row['code'], row['sector'])
            future = executor.submit(daily_trade_info.saveDailyTradeInfo, row['code'], row['sector'])
            task_list.append(future)
        concurrent.futures.wait(task_list)

def historyTRINIndex_2():
    """
    calculate daily index
    :return:
    """


if __name__ == "__main__":
    currentTRINIndex()
    # saveStockList()
    # historyTRINIndex_1()
    # historyTRINIndex_2()







