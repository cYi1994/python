#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import datetime
import csv
import smtplib
import email.MIMEBase
import os.path

# --- 天润数据 ---

today = datetime.date.today()
delta_days = datetime.timedelta(days=1)
yesterday = today - delta_days
print yesterday

db = MySQLdb.connect(host='',
                     port=,
                     user='',
                     passwd='',
                     db='')

cur = db.cursor()

sql = ('SELECT date_format(from_unixtime(c.start_time), "%Y-%m-%d") as "日期",\
            c.client_name as "咨询师姓名",\
            count(c.customer_number) as "呼出数",\
            sum(if(c.status = 21, 1, 0)) as "未接通数",\
            sum(if(c.status = 22, 1, 0)) as "无效数",\
            sum(if(c.status = 24, 1, 0)) as "座席未接通数",\
            sum(if(c.status = 28, 1, 0)) as "接通数",\
            sum(if(c.status = 28,c.total_duration,0))/60 as "接通通话总时长"\
        FROM crm_call_outcome_record c\
        WHERE date_format(from_unixtime(c.start_time), "%Y-%m-%d") = "{0}"\
        GROUP BY c.client_name,date_format(from_unixtime(c.start_time), "%Y-%m-%d")\
        order by date_format(from_unixtime(c.start_time), "%Y-%m-%d");').format(yesterday)
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

headers = ['日期', '咨询师姓名', '呼出数', '未接通数', '无效数', '座席未接通数', '接通数', '接通通话时长']
yest_in_name = datetime.datetime.strftime(yesterday, '%m_%d')
datafile_name1 = 'tianrun_outcome_%s.csv' % yest_in_name

with open(datafile_name1, 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(a)

cur.close()
db.close()

# --- 今日试听邀约 ---

db = MySQLdb.connect(host='',
                     port=,
                     user='',
                     passwd='',
                     db='')

cur = db.cursor()

sql = ('SELECT n1.t1 as "日期", n1.client_name as "咨询师姓名", count(n1.pid) as "试听邀约数"\
        FROM\
        (\
        SELECT DATE_FORMAT(FROM_UNIXTIME(p.create_time), "%Y-%m-%d") as t1,\
                        n.client_name,\
                        p.pid\
        FROM tutor_preorder p\
        LEFT JOIN\
        (\
        SELECT distinct u.user_id, c.client_name\
        FROM user_online u\
        JOIN crm_call_outcome_record c ON u.telephone_num = c.customer_number\
        ) as n\
        ON p.student_user_id = n.user_id\
        WHERE date_format(from_unixtime(create_time), "%Y-%m-%d") = "{0}"\
            AND p.name not like "题目%"\
            AND p.name not like "测试%"\
            AND p.content not like "内容%"\
            AND p.content not like "测试%"\
            AND p.status <> "CANCEL"\
            AND p.category <> "SERIES"\
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
        ) as n1\
        GROUP BY n1.t1, n1.client_name;').format(yesterday)
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

headers = ['日期', '咨询师姓名', '试听邀约数']
yest_in_name = datetime.datetime.strftime(yesterday, '%m_%d')
datafile_name2 = 'create_preorder_sales_%s.csv' % yest_in_name

with open(datafile_name2, 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(a)

cur.close()
db.close()

# --- 今日预计试听 ---

db = MySQLdb.connect(host='',
                     port=,
                     user='',
                     passwd='',
                     db='')

cur = db.cursor()

sql = ('SELECT n1.t1 as "日期", n1.client_name as "咨询师姓名", count(n1.pid) as "今日预计试听数"\
        FROM\
        (\
        SELECT DATE_FORMAT(FROM_UNIXTIME(p.start_time), "%Y-%m-%d") as t1,\
                        n.client_name,\
                        p.pid\
        FROM tutor_preorder p\
        LEFT JOIN\
        (\
        SELECT distinct u.user_id, c.client_name\
        FROM user_online u\
        JOIN crm_call_outcome_record c ON u.telephone_num = c.customer_number\
        ) as n\
        ON p.student_user_id = n.user_id\
        WHERE date_format(from_unixtime(p.start_time), "%Y-%m-%d") = "{0}"\
            AND p.name not like "题目%"\
            AND p.name not like "测试%"\
            AND p.content not like "内容%"\
            AND p.content not like "测试%"\
            AND p.status <> "CANCEL"\
            AND p.category <> "SERIES"\
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
        ) as n1\
        GROUP BY n1.t1, n1.client_name;').format(yesterday)
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

headers = ['日期', '咨询师姓名', '今日预计试听数']
yest_in_name = datetime.datetime.strftime(yesterday, '%m_%d')
datafile_name3 = 'start_preorder_sales_%s.csv' % yest_in_name

with open(datafile_name3, 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(a)

cur.close()
db.close()

# --- 今日试听完成 ---

db = MySQLdb.connect(host='',
                     port=,
                     user='',
                     passwd='',
                     db='')

cur = db.cursor()

sql = ('SELECT n1.t1 as "日期", n1.client_name as "咨询师姓名", count(n1.pid) as "今日试听完成数"\
        FROM\
        (\
        SELECT DATE_FORMAT(FROM_UNIXTIME(p.start_time), "%Y-%m-%d") as t1,\
                        n.client_name,\
                        p.pid\
        FROM tutor_preorder p\
        LEFT JOIN\
                        (\
                        SELECT distinct u.user_id, c.client_name\
                        FROM user_online u\
                        JOIN crm_call_outcome_record c ON u.telephone_num = c.customer_number\
                        ) as n\
        ON p.student_user_id = n.user_id\
        LEFT JOIN audio_record_info a ON p.tutor_record_id = a.tutor_record_id\
        WHERE date_format(from_unixtime(p.start_time), "%Y-%m-%d") = "{0}"\
            AND p.status NOT LIKE "CANCEL"\
            AND p.category <> "SERIES"\
            AND p.name not like "题目%"\
            AND p.content not like "内容%"\
            AND p.name NOT LIKE "测试%"\
            AND p.content NOT LIKE "测试%"\
            AND p.tutor_record_id = a.tutor_record_id\
            AND from_unixtime(floor(a.start_time/1000)) IS NOT NULL\
            AND round((a.end_time-a.start_time)/60000) > 15\
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
        ) as n1\
        GROUP BY n1.t1, n1.client_name').format(yesterday)
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

headers = ['日期', '咨询师姓名', '今日试听完成数']
yest_in_name = datetime.datetime.strftime(yesterday, '%m_%d')
datafile_name4 = 'finished_preorder_sales_%s.csv' % yest_in_name

with open(datafile_name4, 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(a)

cur.close()
db.close()

# --- 每日成单数据 ---

db = MySQLdb.connect(host='',
                     port=,
                     user='',
                     passwd='',
                     db='')

cur = db.cursor()

sql = ('SELECT DISTINCT pid,\
                from_unixtime(update_time),\
                name,\
                student_user_id,\
                planner_name,\
                lesson_num,\
                amount/100,\
                original_amount/100,\
                note\
        FROM series_order\
        WHERE date_format(from_unixtime(update_time), "%Y-%m-%d") = "{0}"\
          AND (note NOT LIKE "%zyb%")\
          AND (name NOT LIKE "%测试%")\
          AND (name NOT LIKE "%test%")\
          and status ="SUCCESS"\
          AND amount/100>100\
          AND student_user_id NOT IN (148811250,\
                                      141321906,\
                                      141321906,\
                                      43744461,\
                                      250595181,\
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
                                      88452392,\
                                      122839998,\
                                      247444506)').format(yesterday)
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

headers = ['日期', '咨询师姓名', '今日试听完成数']
yest_in_name = datetime.datetime.strftime(yesterday, '%m_%d')
datafile_name5 = 'series_order_%s.csv' % yest_in_name

with open(datafile_name5, 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(a)

cur.close()
db.close()

# --- 加附件，发邮件 ---
From = "chuan.yi@lejent.com"  # 登陆邮箱
To = "john@lejent.com"  # 收件人邮箱
password = ''

server = smtplib.SMTP("smtp.exmail.qq.com")
server.login(From, password)  # 仅smtp服务器需要验证时

# 构造MIMEMultipart对象做为根容器
main_msg = email.MIMEMultipart.MIMEMultipart()

# 构造MIMEText对象做为邮件显示内容并附加到根容器
text_msg = email.MIMEText.MIMEText("This is Chuan's heritage")
main_msg.attach(text_msg)

# 构造MIMEBase对象做为文件附件内容并附加到根容器
contype = 'application/octet-stream'
maintype, subtype = contype.split('/', 1)

## 读入文件内容并格式化 ## 设置附件头
data = open(datafile_name1, 'rb')
file_msg1 = email.MIMEBase.MIMEBase(maintype, subtype)
file_msg1.set_payload(data.read())
data.close()
email.Encoders.encode_base64(file_msg1)

basename1 = os.path.basename(datafile_name1)
file_msg1.add_header('Content-Disposition',
                    'attachment', filename=basename1)
main_msg.attach(file_msg1)
# ----------------------------------------
data = open(datafile_name2, 'rb')
file_msg2 = email.MIMEBase.MIMEBase(maintype, subtype)
file_msg2.set_payload(data.read())
data.close()
email.Encoders.encode_base64(file_msg2)

basename2 = os.path.basename(datafile_name2)
file_msg2.add_header('Content-Disposition',
                    'attachment', filename=basename2)
main_msg.attach(file_msg2)
# ----------------------------------------
data = open(datafile_name3, 'rb')
file_msg3 = email.MIMEBase.MIMEBase(maintype, subtype)
file_msg3.set_payload(data.read())
data.close()
email.Encoders.encode_base64(file_msg3)

basename3 = os.path.basename(datafile_name3)
file_msg3.add_header('Content-Disposition',
                    'attachment', filename=basename3)
main_msg.attach(file_msg3)
# ----------------------------------------
data = open(datafile_name4, 'rb')
file_msg4 = email.MIMEBase.MIMEBase(maintype, subtype)
file_msg4.set_payload(data.read())
data.close()
email.Encoders.encode_base64(file_msg4)

basename4 = os.path.basename(datafile_name4)
file_msg4.add_header('Content-Disposition',
                    'attachment', filename=basename4)
main_msg.attach(file_msg4)
# ----------------------------------------
data = open(datafile_name5, 'rb')
file_msg5 = email.MIMEBase.MIMEBase(maintype, subtype)
file_msg5.set_payload(data.read())
data.close()
email.Encoders.encode_base64(file_msg5)

basename5 = os.path.basename(datafile_name5)
file_msg5.add_header('Content-Disposition',
                    'attachment', filename=basename5)
main_msg.attach(file_msg5)
# ----------------------------------------

# 设置根容器属性
main_msg['From'] = From
main_msg['To'] = To
main_msg['Subject'] = "%s data support" % yesterday
main_msg['Date'] = email.Utils.formatdate()

# 得到格式化后的完整文本
fullText = main_msg.as_string()

# 用smtp发送邮件
try:
    server.sendmail(From, To, fullText)
    print 'ok'
finally:
    server.quit()
# --- * ---
