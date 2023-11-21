import datetime
import chinese_calendar

def get_closest_workday(year, month, day):
    """
    指定日期的最近工作日，日期往后找
    :param year:
    :param month:
    :param day:
    :return:
    """
    if isinstance(month, str):
        month = int(month)
    date = datetime.date(year, month, day)
    max_c = 365
    c = 0
    while True:
        holiday = chinese_calendar.is_holiday(date)
        weekday = date.weekday()
        if not holiday and weekday != 5 and weekday != 6:
            return date
        date = date + datetime.timedelta(days=1)
        c += 1 # 防止循环不停止
        if c > max_c:
            raise Exception('Max Date Count!')

def get_target_day(year, month, weekday_num, week_num):
    """
    指定月份的第week_num个星期x的日期
    :param year: 年
    :param month: 月
    :param weekday_num: 从0到6，0-周一，1-周二，2-周三，3-周四，4-周五，5-周六，6-周日
    :param week_num: 这个月的第几周，从1开始
    :return: 日期
    """
    if isinstance(month, str):
        month = int(month)
    date = datetime.datetime(year, month, 1)
    # 找到第1个星期weekday_num
    while date.weekday() != weekday_num:  # 0表示星期一，6表示星期日，4表示星期五
        date += datetime.timedelta(days=1)
    # 再找第week_num个周
    for _ in range(week_num - 1):
        date += datetime.timedelta(days=7)
    return date


if __name__ == "__main__":
    date = datetime.date(2012, 10, 1)
    result = chinese_calendar.is_holiday(date)
    print(f"{date}是节假日吗？{result}")
    date1 = datetime.date(2012, 10, 9)
    result1 = chinese_calendar.is_workday(date1)
    print(f"{date1}是工作日吗？{result1}")
    result2 = get_target_day(2023, 7, 4, 3)
    print(f"2023-7月第3个星期五是：{result2}")
    result3 = get_closest_workday(result2.year, result2.month, result2.day)
    print(f"{result2}最近的工作日是：{result3}")
