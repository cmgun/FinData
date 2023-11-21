import os
import zipfile
import pandas as pd

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

path = '../../data/CFFEX/'

def upzipFile(filename):
    # 判断文件是否存在
    file_path = path + filename + '.zip'
    if not os.path.exists(file_path):
        print(file_path + '文件不存在')
        return
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(path + filename)
        print(file_path + '解压成功')

if __name__ == "__main__":
    # 解压数据
    for index in range(23, 24):
        for m in range(len(months)):
            year = '20' + str(index)
            month = months[m]
            filename = year + month
            upzipFile(filename)


