#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import datetime
import csv
import smtplib
import email.MIMEBase
import os.path

today = datetime.date.today()
delta_days = datetime.timedelta(days=1)
yesterday = today - delta_days
print yesterday

db = MySQLdb.connect(host='101.200.162.245',
                     port=3308,
                     user='youzhangwei',
                     passwd='Aftyouzw4rjm',
                     db='afanti_online')
cur = db.cursor()

sql = ('SELECT from_unixtime(p.create_time) AS "试听课创建时间",\
               p.student_user_id,\
               p.teacher_user_id,\
               p.status AS "预约状态",\
               t.tutor_status as "上课状态",\
               from_unixtime(p.start_time) AS "预约上课时间",\
               from_unixtime(floor(a.start_time/1000)) AS "课程录音开始时间",\
               if(a.end_time>0,from_unixtime(floor(a.end_time/1000)),"") AS "课程录音结束时间",\
               p.tutor_record_id AS "上课辅导记录ID",\
               if(a.end_time>a.start_time,round((a.end_time-a.start_time)/60000,2),0) AS "录音时长",\
               t.ua AS "设备号",\
               CASE\
                   WHEN t.ua LIKE "%android%" THEN "android"\
                   WHEN t.ua LIKE "%iOS%" THEN "iOS"\
                   ELSE "PC"\
               END AS "设备信息",\
               p.grade as grade,\
               p.subject as subject,\
               n1.client_name as "咨询师姓名",\
               n2.user_name as "老师姓名",\
               n2.telephone_num as "老师手机",\
               n2.province as "老师省份",\
               n2.city as "老师城市"\
        FROM tutor_preorder p\
        JOIN tutor_record t ON p.tutor_record_id=t.tutor_record_id\
        LEFT JOIN audio_record_info a ON p.tutor_record_id=a.tutor_record_id\
        LEFT JOIN\
        (\
        SELECT DISTINCT u1.user_id, c.client_name\
        FROM user_online u1\
        JOIN crm_call_outcome_record c ON c.customer_number = u1.telephone_num\
        WHERE c.status = 28\
        GROUP BY u1.user_id\
        HAVING MAX(c.start_time)\
        ) as n1 ON n1.user_id = p.student_user_id\
        LEFT JOIN\
        (\
        SELECT distinct u2.user_id, u2.user_name, u2.telephone_num, u2.province, u2.city\
        FROM user_online u2\
        ) as n2 ON n2.user_id = p.teacher_user_id\
        WHERE p.category="DEMO"\
          AND p.status ="BOOK"\
          AND t.tutor_status>0\
          AND p.name NOT LIKE"%测试%"\
          AND from_unixtime(floor(a.start_time/1000)) IS NOT NULL\
          AND if(a.end_time>a.start_time,round((a.end_time-a.start_time)/60000,2),0)>10\
          AND date_format(from_unixtime(p.start_time), "%Y-%m-%d") = "{0}"\
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
        ORDER BY p.start_time').format(yesterday)
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
           '老师ID', '预约状态', '是否上课', '预约上课时间', '课程录音开始时间', '课程录音结束时间', '上课辅导记录ID', '录音时长',
           '试听设备', '设备',
           'GRADE', 'SUBJECT', '咨询师姓名',
           '老师姓名', '老师手机', '老师省份', '老师城市']
yest_in_name = datetime.datetime.strftime(yesterday, '%m_%d')
datafile_name = 'preorder_finished_%s.csv' % yest_in_name
with open(datafile_name, 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(a)

cur.close()
db.close()

# --- 加附件，发邮件 ---
From = "chuan.yi@lejent.com"  # 登陆邮箱
To = "marc.lin@lejent.com"  # 收件人邮箱


server = smtplib.SMTP("smtp.exmail.qq.com")
server.login(From, "Malilan123")  # 仅smtp服务器需要验证时

# 构造MIMEMultipart对象做为根容器
main_msg = email.MIMEMultipart.MIMEMultipart()

# 构造MIMEText对象做为邮件显示内容并附加到根容器
text_msg = email.MIMEText.MIMEText("This is Chuan's heritage")
main_msg.attach(text_msg)

# 构造MIMEBase对象做为文件附件内容并附加到根容器
contype = 'application/octet-stream'
maintype, subtype = contype.split('/', 1)

## 读入文件内容并格式化
data = open(datafile_name, 'rb')
file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
file_msg.set_payload(data.read())
data.close()
email.Encoders.encode_base64(file_msg)

## 设置附件头
basename = os.path.basename(datafile_name)
file_msg.add_header('Content-Disposition',
                    'attachment', filename=basename)
main_msg.attach(file_msg)

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
