"""
(Emotional Index) Get current TRIN index
TRIN = (declined_amount / declined_count) / (advanced_amount / advanced_count)
"""
import stock_list
import datetime
import pandas as pd

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
    df = pd.DataFrame(columns=['code'])
    for stock in stocks:
        data = {'code': stock['code']}
        df = pd.concat([df, pd.DataFrame(data, index=[0])], ignore_index=True)
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
            advanced_amt += stock['volume']
        elif stock['%change'] < 0:
            declined_cnt += 1
            declined_amt += stock['volume']
    trin = (declined_amt / declined_cnt) / (advanced_amt / advanced_cnt)
    print(f'time: {formatted_time}, TRIN: {trin}')


if __name__ == "__main__":
    currentTRINIndex()
    # saveStockList()





