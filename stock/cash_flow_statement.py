"""
Query cash flow statement by quarter
"""
import requests
import json
import pandas as pd
import share_list as sl
import datetime


def get_cash_flow_statement(code, sector):
    """
    return params list
    1. Cash flow from operating activities, 经营活动产生的现金流量
    SALES_SERVICES: Cash received from selling goods and providing services, 销售商品、提供劳务收到的现金
    RECEIVE_TAX_REFUND: Tax refund received, 收到的税收返还
    RECEIVE_OTHER_OPERATE: Other cash received related to operating activities, 收到其他与经营活动有关的现金
    BUY_SERVICES: Cash used to purchase goods and receive services, 购买商品、接受劳务支付的现金
    PAY_STAFF_CASH: Cash payments to and for employees, 支付给职工以及为职工支付的现金
    PAY_ALL_TAX: Various taxes paid, 支付的各项税费
    PAY_OTHER_OPERATE: Other cash payments related to operating activities, 支付其他与经营活动有关的现金
    NETCASH_OPERATE: Net cash flow from operating activities, 经营活动产生的现金流量净额
    2. Cash flows from investing activities, 投资活动产生的现金流量
    WITHDRAW_INVEST: Recover cash received on investment, 收回投资收到的现金
    RECEIVE_INVEST_INCOME: Cash received from investment income, 取得投资收益收到的现金
    DISPOSAL_LONG_ASSET: Net cash received from disposal of fixed assets, intangible assets and other long-term assets, 处置固定资产、无形资产和其他长期资产收回的现金净额
    RECEIVE_OTHER_INVEST: Other cash received related to investing activities, 收到的其他与投资活动有关的现金
    CONSTRUCT_LONG_ASSET: Cash paid for the purchase and construction of fixed assets, intangible assets and other long-term assets, 购建固定资产、无形资产和其他长期资产支付的现金
    INVEST_PAY_CASH: Cash Investment, 投资支付的现金
    OBTAIN_SUBSIDIARY_OTHER: Net cash received from subsidiaries and other business units, 取得子公司及其他营业单位支付的现金净额
    NETCASH_INVEST: Net cash flows from investing activities, 投资活动产生的现金流量净额
    3. cash flow from financing activities, 筹资活动产生的现金流量
    RECEIVE_LOAN_CASH: Obtain cash received from borrowing money, 取得借款收到的现金
    RECEIVE_OTHER_FINANCE: Other cash received related to financing activities, 收到的其他与筹资活动有关的现金
    PAY_DEBT_CASH:Cash paid to repay debt, 偿还债务所支付的现金
    ASSIGN_DIVIDEND_PORFIT: Cash paid to distribute dividends, profits or repay interest, 分配股利、利润或偿付利息支付的现金
    PAY_OTHER_FINANCE: Other cash payments related to financing activities, 支付的其他与筹资活动有关的现金
    NETCASH_FINANCE: Net cash flow from financing activities, 筹资活动产生的现金流量净额
    4.RATE_CHANGE_EFFECT: effect of the changes of the exchange rate on cash and the equivalents, 汇率变动对现金及现金等价物的影响
    5.CCE_ADD: Net increase in cash and cash equivalents, 现金及现金等价物净增加额
    6.BEGIN_CCE: Opening cash and cash equivalents balance, 期初现金及现金等价物余额
    7.END_CCE: Closing cash and cash equivalents balance, 期末现金及现金等价物余额

    :param code:
    :return:
    """
    url = 'https://datacenter.eastmoney.com/securities/api/data/get'
    # report date range: last five years
    report_date = get_last_x_year(8)
    page_no = 1
    if sector == 0:
        sector = 'SZ'
    elif sector == 1:
        sector = 'SH'
    else:
        sector = 'BJ'
    params = {
        'type': 'RPT_F10_FINANCE_GCASHFLOWQC',
        'sty': 'APP_F10_GCASHFLOWQC',
        'filter': f'(SECUCODE="{code}.{sector}")(REPORT_DATE in ({report_date}))',
            'p': {page_no},
        'ps': 100,
        'sr': -1,
        'st': 'REPORT_DATE',
        'source': 'HSF10',
        'client': 'PC',
        'v': '0192148313797750'
    }
    response = requests.get(url, params)
    if response.status_code == 200:
        resp = json.loads(response.text)
        try:
            pages = resp['result']['pages']
            reports = resp['result']['data']
        except Exception as e:
            # 处理其他类型的异常
            print(f"发生了异常: {e}")
            return []
        while pages > 1:
            page_no += 1
            params['pn'] = page_no
            response = requests.get(url, params)
            resp = json.loads(response.text)
            if len(resp['result']['data']) > 0:
                reports.append(resp['result']['data'])
            pages -= 1
        return reports
    else:
        print(f'查询失败,url:{url}')
    return []

def get_last_x_year(x):
    """
    get query date
    :param x:
    :return:
    """
    current_year = datetime.date.today().year
    quarter = ['-03-31', '-06-30', '-09-30', '-12-31']
    result_str = ''
    for i in range(0, x):
        year = current_year - i
        for date in quarter:
            result = '\'' + str(year) + date + '\''
            result_str = result_str + ',' + result
    return result_str[1:]


def store_data(reports, code):
    if len(reports) <= 0:
        return
    file_name = f'../data/stock/cash_flow_statement_{code}.csv'
    df = pd.DataFrame(columns=['DATE', 'NAME', 'SALES_SERVICES', 'RECEIVE_TAX_REFUND', 'RECEIVE_OTHER_OPERATE', 'BUY_SERVICES', 'PAY_STAFF_CASH', 'PAY_ALL_TAX', 'PAY_OTHER_OPERATE', 'NETCASH_OPERATE',
                               'WITHDRAW_INVEST', 'RECEIVE_INVEST_INCOME', 'DISPOSAL_LONG_ASSET', 'RECEIVE_OTHER_INVEST', 'CONSTRUCT_LONG_ASSET', 'INVEST_PAY_CASH', 'OBTAIN_SUBSIDIARY_OTHER', 'NETCASH_INVEST',
                               'RECEIVE_LOAN_CASH', 'RECEIVE_OTHER_FINANCE', 'PAY_DEBT_CASH', 'ASSIGN_DIVIDEND_PORFIT', 'PAY_OTHER_FINANCE', 'NETCASH_FINANCE',
                               'RATE_CHANGE_EFFECT', 'CCE_ADD', 'BEGIN_CCE', 'END_CCE'])
    for info in reports:
        data = {'DATE': info['REPORT_DATE'][:10], 'NAME': info['SECURITY_NAME_ABBR'], 'RECEIVE_TAX_REFUND': info['RECEIVE_TAX_REFUND'], 'SALES_SERVICES': info['SALES_SERVICES'] , 'RECEIVE_OTHER_OPERATE': info['RECEIVE_OTHER_OPERATE'],
                'BUY_SERVICES': info['BUY_SERVICES'], 'PAY_STAFF_CASH': info['PAY_STAFF_CASH'], 'PAY_ALL_TAX': info['PAY_ALL_TAX'], 'PAY_OTHER_OPERATE': info['PAY_OTHER_OPERATE'], 'NETCASH_OPERATE': info['NETCASH_OPERATE'],
                'WITHDRAW_INVEST': info['WITHDRAW_INVEST'], 'RECEIVE_INVEST_INCOME': info['RECEIVE_INVEST_INCOME'], 'DISPOSAL_LONG_ASSET': info['DISPOSAL_LONG_ASSET'], 'RECEIVE_OTHER_INVEST': info['RECEIVE_OTHER_INVEST'], 'CONSTRUCT_LONG_ASSET': info['CONSTRUCT_LONG_ASSET'], 'INVEST_PAY_CASH': info['INVEST_PAY_CASH'], 'OBTAIN_SUBSIDIARY_OTHER': info['OBTAIN_SUBSIDIARY_OTHER'], 'NETCASH_INVEST': info['NETCASH_INVEST'],
                'RECEIVE_LOAN_CASH': info['RECEIVE_LOAN_CASH'], 'RECEIVE_OTHER_FINANCE': info['RECEIVE_OTHER_FINANCE'], 'PAY_DEBT_CASH': info['PAY_DEBT_CASH'], 'ASSIGN_DIVIDEND_PORFIT': info['ASSIGN_DIVIDEND_PORFIT'], 'PAY_OTHER_FINANCE': info['PAY_OTHER_FINANCE'], 'NETCASH_FINANCE': info['NETCASH_FINANCE'],
                'RATE_CHANGE_EFFECT': info['RATE_CHANGE_EFFECT'], 'CCE_ADD': info['CCE_ADD'], 'BEGIN_CCE': info['BEGIN_CCE'], 'END_CCE': info['END_CCE']
                }
        df = pd.concat([df, pd.DataFrame(data, index=[0])], ignore_index=True)
    df.to_csv(file_name)
    print(f'stored {file_name} successfully.')

if __name__ == "__main__":
    code_list = sl.get_share_list('BK1037')
    for code_info in code_list:
        reports = get_cash_flow_statement(code_info['code'], code_info['sector'])
        store_data(reports, code_info['code'])

    # code = '600745'
    # # 0-SZ, 1-SH
    # sector = 1

