#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/4/7 10:46
software: PyCharm
description: 
'''

'''part1'''
# from redis import StrictRedis
#
# redis = StrictRedis(host='localhost',port=6379,db=0)
# redis.set('name','bob')
# print(redis.get('name'))


'''part2'''
from redis import StrictRedis,ConnectionPool

pool = ConnectionPool(host='localhost',port=6379,db=0)
redis = StrictRedis(connection_pool=pool)

