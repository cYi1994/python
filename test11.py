#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import datetime
import csv
import smtplib
import email.MIMEBase
import os.path


db = MySQLdb.connect(host='10.44.62.51',
                     port=3308,
                     user='youzhangwei',
                     passwd='Aftyouzw4rjm',
                     db='afanti_online')
cur = db.cursor()

date1 = '2017-08-05'
date2 = '2017-08-07'
sql = ('SELECT from_unixtime(p.create_time) AS "试听课创建时间",\
               p.student_user_id,\
               p.teacher_user_id,\
               p.status AS "预约状态",\
               t.tutor_status as "上课状态",\
               from_unixtime(p.start_time) AS "预约上课时间",\
               p.tutor_record_id AS "上课辅导记录ID",\
               t.ua AS "设备号",\
               CASE\
                   WHEN t.ua LIKE "%android%" THEN "android"\
                   WHEN t.ua LIKE "%iPhone%" THEN "iPhone"\
                   WHEN t.ua LIKE "%iPad%" THEN "iPad"\
                   ELSE "PC"\
               END AS "设备信息",\
               p.grade as grade,\
               p.subject as subject,\
               i.period_confirm\
        FROM tutor_preorder p\
        JOIN tutor_record t ON p.tutor_record_id = t.tutor_record_id\
        LEFT JOIN tutor_preorder_info i ON i.tutor_record_id = t.tutor_record_id\
        WHERE p.category = "DEMO"\
          AND p.name NOT LIKE"%测试%"\
          AND date_format(from_unixtime(p.create_time), "%Y-%m-%d") between "{0}" and "{1}"\
          AND p.student_user_id NOT IN (250595181,\
                                        141321906,\
                                        249450013,\
                                        250595219,\
                                        248444058,\
                                        248259226,\
                                        251804322,\
                                        251804626,\
                                        251804835,\
                                        251436121,\
                                        75462035,\
                                        247444506)\
        ORDER BY p.create_time').format(date1, date2)
cur.execute(sql)
result = cur.fetchall()


a = list()
j = 0
for j in range(len(result)):
    e = 0
    b = list()
    for e in range(len(result[j])):
        b.append(result[j][e])
        print result[j][e],
    a.append(b)
    print len(a), 'rows done'

headers = ['试听课生成时间', '学生ID',
           '老师ID', '预约状态', '是否上课', '预约上课时间', '上课辅导记录ID',
           '试听设备', '设备',
           'GRADE', 'SUBJECT', '是否完成']
yest_in_name = datetime.datetime.strftime(datetime.datetime.now(), '%m_%d')
datafile_name = 'preorder_%s.csv' % yest_in_name
with open(datafile_name, 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(a)

cur.close()
db.close()

