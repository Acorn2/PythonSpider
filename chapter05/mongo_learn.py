#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/13 15:09
software: PyCharm
description: mongodb学习
'''
import pymongo
from bson.objectid import ObjectId

#连接MongoDB
client = pymongo.MongoClient(host='localhost',port=27017)
# client = pymongo.MongoClient()

#指定数据库
db = client.learnTest

#指定集合
collection = db.students

#插入数据
student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}

# 在PyMongo 3.x版本中，官方已经不推荐使用insert()方法了。当然，继续使用也没有什么问题。官方推荐使用insert_one()和insert_many()方法来分别插入单条记录和多条记录
# result = collection.insert_one(student)
# print(result)
# print(result.inserted_id)
#
# student1 = {
#     'id': '20170101',
#     'name': 'Jordan',
#     'age': 20,
#     'gender': 'male'
# }
#
# student2 = {
#     'id': '20170202',
#     'name': 'Mike',
#     'age': 21,
#     'gender': 'male'
# }
#
# result = collection.insert_many([student1, student2])
# print(result)
# print(result.inserted_ids)

#查询 其中find_one()查询得到的是单个结果，find()则返回一个生成器对象。
result = collection.find_one({'name':'Mike'})
print(result)

results = collection.find({'age':20})
for i in results:
    print(i)

#如果要查询年龄大于20的数据
results = collection.find({'age':{'$gt':20}})
for i in results:
    print(i)

#计数
count = collection.find().count()
print(count)

#排序 pymongo.ASCENDING指定升序。如果要降序排列，可以传入pymongo.DESCENDING。
results = collection.find().sort('name',pymongo.ASCENDING)
print([result['name'] for result in results])

#偏移
#利用skip()方法偏移几个位置，比如偏移2，就忽略前两个元素，得到第三个及以后的元素：
results = collection.find().sort('name',pymongo.ASCENDING).skip(2)
print([result['name'] for result in results])

#用limit()方法指定要取的结果个数
results = collection.find().sort('name',pymongo.ASCENDING).skip(2).limit(1)
print([result['name'] for result in results])

collection.find({'_id':{'$gt':ObjectId('5c88af5c0dbcab3828d5b063')}})

#更新

update_data = {'name':'Mike'}
student = collection.find_one(update_data)
student['age'] = 25
result = collection.update_one(update_data,{'$set':student})
print(result)