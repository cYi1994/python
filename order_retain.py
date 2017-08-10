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

sql = 'SELECT DISTINCT pid, \
                from_unixtime(update_time), \
                name, \
                student_user_id, \
                planner_name, \
                lesson_num, \
                amount/100, \
                original_amount/100, \
                parents_name, \
                note \
FROM series_order \
WHERE date_format(from_unixtime(update_time), "%Y-%m-%d") >= "2017-06-01" \
  AND (note NOT LIKE "%zyb%") \
  AND (name NOT LIKE "%测试%") \
  AND (name NOT LIKE "%test%") \
  and status ="SUCCESS" \
  AND amount/100>100 \
  AND student_user_id NOT IN (148811250, \
                              141321906, \
                              141321906, \
                              43744461, \
                              250595181, \
                              141321906, \
                              249450013, \
                              250595219, \
                              248444058, \
                              248259226, \
                              251804322, \
                              251804626, \
                              251804835, \
                              251436121, \
                              75462035, \
                              47444506) \
order by student_user_id'
cur.execute(sql)
result = cur.fetchall()

a = list()
i = 0
for i in range(len(result)):
    e = 0
    b = list()
    for e in range(len(result[i])):
        print result[i][e]
        b.append(result[i][e])
    a.append(b)
print len(a), 'rows done'


with open('order_from_june.csv', 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerows(a)


cur.close()
db.close()
