#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import csv

db = MySQLdb.connect(host='10.44.62.51',
                     port=3308,
                     user='youzhangwei',
                     passwd='Aftyouzw4rjm',
                     db='afanti_online')
cur = db.cursor()

sql = 'select user_id, user_name, telephone_num, province, city\
        from user_online\
        group by user_id'
cur.execute(sql)
result = cur.fetchall()

a = list()
j = 0
for j in range(len(result)):
    e = 0
    b = list()
    for e in range(len(result[j])):
        b.append(result[j][e])
    a.append(b)
    for kk in b:
        print kk
print len(a), 'rows done'

headers = ['user_id', 'user_name', 'telephone_num', 'province', 'city']
with open('user_online.csv', 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(a)


cur.close()
db.close()
