#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/2 10:22
software: PyCharm
description: 
'''
import csv
import pandas as pd

# with open('csv_data.csv','w',encoding='utf-8') as fw:
#     filednames = ['id','name','age']
#     writer = csv.DictWriter(fw,fieldnames=filednames)
#     writer.writeheader()
#     writer.writerow({'id': '10001', 'name': 'Mike', 'age': 20})
#     writer.writerow({'id': '10002', 'name': 'Bob', 'age': 22})
#     writer.writerow({'id': '10003', 'name': 'Jordan', 'age': 21})
#     writer.writerow({'id': '10004', 'name': '王五', 'age': 21})


df = pd.read_csv('csv_data.csv')
print(df)