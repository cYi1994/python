#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import csv

filepath = "order_from_june.csv"
df = pd.read_csv(filepath, names=['pid', 'update_time', 'name', 'student_user_id', 'planner_name', 'lesson_num',
                                  'amount', 'original amount', 'parent', 'note'])

a = list()
b = list()
i = 0
for i in range(len(df['pid'])):
    user_id = df['student_user_id'][i]
    update_time = df['update_time'][i]
    planner_name = df['planner_name'][i]
    lesson_num = int(df['lesson_num'][i])
    amount = int(df['amount'][i])
    if user_id not in b:
        a.append(b)
        b = list()
        b.append(user_id)
        b.append(update_time)
        b.append(planner_name)
        b.append(lesson_num)
        b.append(amount)
        #for k in b:
        #    print k
    else:
        if datetime.datetime.strptime(update_time, '%Y-%m-%d %H:%M:%S') - \
           datetime.datetime.strptime(b[1], '%Y-%m-%d %H:%M:%S') < datetime.timedelta(days=14):
            b[3] = b[3] + lesson_num
            b[4] = b[4] + amount
            #for k in b:
            #    print k
        else:
            a.append(b)
            b = list()
            b.append(user_id)
            b.append(update_time)
            b.append(planner_name)
            b.append(lesson_num)
            b.append(amount)
            #for k in b:
            #    print k
print len(a), 'rows done'

headers = ['student_user_id', 'update_time', 'planner_name', 'lesson_num', 'amount']
with open(u'14天内成单聚合.csv', 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(a)
