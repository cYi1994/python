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
# source = '%app-%'
# print source

# --- database connection如有问题请联系林清 ---
# --- 发件人收件人可修改，改发件人别忘了改密码 ---

# --- app-sqtx0yst ---
# --- 今日新增用户数 ---
a = list()


def danping_daily(source):

    db = MySQLdb.connect(host='101.200.162.245',
                         port=3308,
                         user='youzhangwei',
                         passwd='Aftyouzw4rjm',
                         db='afanti_online')

    cur = db.cursor()
    sql = ('SELECT count(distinct c2.telephone_number) as "今日新增用户数"\
            FROM crm_form_record c2\
            WHERE c2.source LIKE "{0}"\
                AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}";').format(source, yesterday)
    cur.execute(sql)
    result = cur.fetchall()

    # a = list()
    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('new incoming amount')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # --- 今日新增呼出数 ---
    cur = db.cursor()
    sql = ('SELECT count(DISTINCT c1.customer_number) as "今日呼出用户数"\
            FROM crm_call_outcome_record c1\
            JOIN (SELECT distinct c2.source,\
                            c2.telephone_number\
                    FROM crm_form_record c2\
                    WHERE c2.source LIKE "{0}"\
                        AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
            ON c1.customer_number = n.telephone_number\
            WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{1}";').format(source, yesterday)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('new incoming dialed')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # --- 平均跟进时效 ---
    cur = db.cursor()
    sql = ('SELECT sec_to_time(avg(`跟进时间`)) as "平均跟进时效"\
            FROM\
            (\
            SELECT n.source,\
                    c1.customer_number,\
                    from_unixtime(max(n.create_time)) as "电话创建时间",\
                    from_unixtime(min(c1.start_time)) as "电话第一次拨出时间",\
                    (c1.start_time - n.create_time) as "跟进时间"\
            FROM crm_call_outcome_record c1\
            JOIN (SELECT distinct c2.telephone_number,\
                                    c2.create_time,\
                                    c2.source\
                    FROM crm_form_record c2\
                    WHERE c2.source LIKE "{0}"\
                        AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
            ON c1.customer_number = n.telephone_number\
            WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{1}"\
                AND sec_to_time(c1.start_time-n.create_time) > 0\
            GROUP BY c1.customer_number\
            ORDER BY from_unixtime(max(n.create_time))\
            ) as n1\
            ORDER BY `平均跟进时效`;').format(source, yesterday)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('follow up efficiency')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # --- 客户未接通数 ---
    cur = db.cursor()
    sql = ('SELECT count(c1.customer_number) as "客户未接通数"\
            FROM crm_call_outcome_record c1\
            JOIN (SELECT distinct c2.source,\
                            c2.telephone_number\
                    FROM crm_form_record c2\
                    WHERE c2.source LIKE "{0}"\
                        AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
            ON c1.customer_number = n.telephone_number\
            WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{1}"\
                AND c1.status = "21"').format(source, yesterday)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('unanswered')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # --- 无效数 ---
    cur = db.cursor()
    sql = ('SELECT count(c1.customer_number) as "无效数"\
            FROM crm_call_outcome_record c1\
            JOIN (SELECT distinct c2.source,\
                            c2.telephone_number\
                    FROM crm_form_record c2\
                    WHERE c2.source LIKE "{0}"\
                        AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
            ON c1.customer_number = n.telephone_number\
            WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{1}"\
                AND c1.status = "22"').format(source, yesterday)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('invalid')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # --- 座席未接通数 ---
    cur = db.cursor()
    sql = ('SELECT count(c1.customer_number) as "座席未接通数"\
            FROM crm_call_outcome_record c1\
            JOIN (SELECT distinct c2.source,\
                            c2.telephone_number\
                    FROM crm_form_record c2\
                    WHERE c2.source LIKE "{0}"\
                        AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
            ON c1.customer_number = n.telephone_number\
            WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{1}"\
                AND c1.status = "24"').format(source, yesterday)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('sales unanswered')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # --- 接通数 ---
    cur = db.cursor()
    sql = ('SELECT count(c1.customer_number) as "接通数"\
            FROM crm_call_outcome_record c1\
            JOIN (SELECT distinct c2.source,\
                            c2.telephone_number\
                    FROM crm_form_record c2\
                    WHERE c2.source LIKE "{0}"\
                        AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
            ON c1.customer_number = n.telephone_number\
            WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{1}"\
                AND c1.status = "28"').format(source, yesterday)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('talked')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # --- 当日试听邀约数 ---
    cur = db.cursor()
    sql = ('SELECT COUNT(DISTINCT student_user_id) AS "当日试听邀约数"\
            FROM tutor_preorder\
            JOIN (\
                    SELECT j1.source,\
                            (u.user_id) as t2\
                    FROM user_online u\
                    JOIN\
                        (\
                        SELECT n.source,\
                                (c1.customer_number) as t1\
                        FROM crm_call_outcome_record c1\
                        JOIN (SELECT distinct c2.source,\
                                                c2.telephone_number\
                                FROM crm_form_record c2\
                                WHERE c2.source LIKE "{0}"\
                                    AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
                        ON c1.customer_number = n.telephone_number\
                        WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{1}"\
                            AND c1.status = "28"\
                        ) as j1\
                    ON u.telephone_num = j1.t1\
                    ) as j2\
            ON student_user_id = j2.t2\
            WHERE status NOT LIKE "CANCEL"\
                AND name NOT LIKE "测试%"\
                AND content NOT LIKE "测试%";').format(source, yesterday)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('preorder created')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()
    db.close()

    # -------------------------------------------
source = '%app-%'
print source
danping_daily(source)
source = '%fdbanner%'
print source
danping_daily(source)
source = '%ps0719%'
print source
danping_daily(source)
source = '%ps0728%'
print source
danping_daily(source)
source = '%sy0710%'
print source
danping_daily(source)
source = '%sy0708%'
print source
danping_daily(source)
source = '%syfeed%'
print source
danping_daily(source)
# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
# --- database connection如有问题请联系林清 ---
# --- 发件人收件人可修改，改发件人别忘了改密码 ---
source = '%即时辅导%'
print source
# --- 即时辅导 ---
delta_days = datetime.timedelta(days=1)
day_before_yesterday = yesterday - delta_days
print day_before_yesterday
# --- 今日新增用户数 ---
db = MySQLdb.connect(host='101.200.162.245',
                     port=3308,
                     user='youzhangwei',
                     passwd='Aftyouzw4rjm',
                     db='afanti_online')

cur = db.cursor()
sql = ('SELECT count(distinct c2.telephone_number) as "今日新增用户数"\
        FROM crm_form_record c2\
        WHERE c2.source LIKE "{0}"\
            AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}";').format(source, day_before_yesterday)
cur.execute(sql)
result = cur.fetchall()

j = 0
for j in range(len(result)):
    e = 0
    b = list()
    for e in range(len(result[j])):
        b.append(source)
        b.append('new incoming amount')
        b.append(result[j][e])
        print result[j][e],
    a.append(b)
    print len(a), 'rows done'
cur.close()

# --- 今日新增呼出数 ---
cur = db.cursor()
sql = ('SELECT count(DISTINCT c1.customer_number) as "今日呼出用户数"\
        FROM crm_call_outcome_record c1\
        JOIN (SELECT distinct c2.source,\
                        c2.telephone_number\
                FROM crm_form_record c2\
                WHERE c2.source LIKE "{0}"\
                    AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
        ON c1.customer_number = n.telephone_number\
        WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{1}";').format(source, day_before_yesterday)
cur.execute(sql)
result = cur.fetchall()

j = 0
for j in range(len(result)):
    e = 0
    b = list()
    for e in range(len(result[j])):
        b.append(source)
        b.append('new incoming dialed')
        b.append(result[j][e])
        print result[j][e],
    a.append(b)
    print len(a), 'rows done'
cur.close()

# --- 平均跟进时效 ---
cur = db.cursor()
sql = ('SELECT sec_to_time(avg(`跟进时间`)) as "平均跟进时效"\
        FROM\
        (\
        SELECT n.source,\
                c1.customer_number,\
                from_unixtime(max(n.create_time)) as "电话创建时间",\
                from_unixtime(min(c1.start_time)) as "电话第一次拨出时间",\
                (c1.start_time - n.create_time) as "跟进时间"\
        FROM crm_call_outcome_record c1\
        JOIN (SELECT distinct c2.telephone_number,\
                                c2.create_time,\
                                c2.source\
                FROM crm_form_record c2\
                WHERE c2.source LIKE "{0}"\
                    AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
        ON c1.customer_number = n.telephone_number\
        WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{2}"\
            AND sec_to_time(c1.start_time-n.create_time) > 0\
        GROUP BY c1.customer_number\
        ORDER BY from_unixtime(max(n.create_time))\
        ) as n1\
        ORDER BY `平均跟进时效`;').format(source, day_before_yesterday, yesterday)
cur.execute(sql)
result = cur.fetchall()

j = 0
for j in range(len(result)):
    e = 0
    b = list()
    for e in range(len(result[j])):
        b.append(source)
        b.append('follow up efficiency')
        b.append(result[j][e])
        print result[j][e],
    a.append(b)
    print len(a), 'rows done'
cur.close()

# --- 客户未接通数 ---
cur = db.cursor()
sql = ('SELECT count(c1.customer_number) as "客户未接通数"\
        FROM crm_call_outcome_record c1\
        JOIN (SELECT distinct c2.source,\
                        c2.telephone_number\
                FROM crm_form_record c2\
                WHERE c2.source LIKE "{0}"\
                    AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
        ON c1.customer_number = n.telephone_number\
        WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{2}"\
            AND c1.status = "21"').format(source, day_before_yesterday, yesterday)
cur.execute(sql)
result = cur.fetchall()

j = 0
for j in range(len(result)):
    e = 0
    b = list()
    for e in range(len(result[j])):
        b.append('JiShiFuDao')
        b.append('unanswered')
        b.append(result[j][e])
        print result[j][e],
    a.append(b)
    print len(a), 'rows done'
cur.close()

# --- 无效数 ---
cur = db.cursor()
sql = ('SELECT count(c1.customer_number) as "无效数"\
        FROM crm_call_outcome_record c1\
        JOIN (SELECT distinct c2.source,\
                        c2.telephone_number\
                FROM crm_form_record c2\
                WHERE c2.source LIKE "{0}"\
                    AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
        ON c1.customer_number = n.telephone_number\
        WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{2}"\
            AND c1.status = "22"').format(source, day_before_yesterday, yesterday)
cur.execute(sql)
result = cur.fetchall()

j = 0
for j in range(len(result)):
    e = 0
    b = list()
    for e in range(len(result[j])):
        b.append('JiShiFuDao')
        b.append('invalid')
        b.append(result[j][e])
        print result[j][e],
    a.append(b)
    print len(a), 'rows done'
cur.close()

# --- 座席未接通数 ---
cur = db.cursor()
sql = ('SELECT count(c1.customer_number) as "座席未接通数"\
        FROM crm_call_outcome_record c1\
        JOIN (SELECT distinct c2.source,\
                        c2.telephone_number\
                FROM crm_form_record c2\
                WHERE c2.source LIKE "{0}"\
                    AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
        ON c1.customer_number = n.telephone_number\
        WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{2}"\
            AND c1.status = "24"').format(source, day_before_yesterday, yesterday)
cur.execute(sql)
result = cur.fetchall()

j = 0
for j in range(len(result)):
    e = 0
    b = list()
    for e in range(len(result[j])):
        b.append('JiShiFuDao')
        b.append('sales unanswered')
        b.append(result[j][e])
        print result[j][e],
    a.append(b)
    print len(a), 'rows done'
cur.close()

# --- 接通数 ---
cur = db.cursor()
sql = ('SELECT count(c1.customer_number) as "接通数"\
        FROM crm_call_outcome_record c1\
        JOIN (SELECT distinct c2.source,\
                        c2.telephone_number\
                FROM crm_form_record c2\
                WHERE c2.source LIKE "{0}"\
                    AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
        ON c1.customer_number = n.telephone_number\
        WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{2}"\
            AND c1.status = "28"').format(source, day_before_yesterday, yesterday)
cur.execute(sql)
result = cur.fetchall()

j = 0
for j in range(len(result)):
    e = 0
    b = list()
    for e in range(len(result[j])):
        b.append('JiShiFuDao')
        b.append('talked')
        b.append(result[j][e])
        print result[j][e],
    a.append(b)
    print len(a), 'rows done'
cur.close()

# --- 当日试听邀约数 ---
cur = db.cursor()
sql = ('SELECT COUNT(DISTINCT student_user_id) AS "当日试听邀约数"\
        FROM tutor_preorder\
        JOIN (\
                SELECT j1.source,\
                        (u.user_id) as t2\
                FROM user_online u\
                JOIN\
                    (\
                    SELECT n.source,\
                            (c1.customer_number) as t1\
                    FROM crm_call_outcome_record c1\
                    JOIN (SELECT distinct c2.source,\
                                            c2.telephone_number\
                            FROM crm_form_record c2\
                            WHERE c2.source LIKE "{0}"\
                                AND date_format(from_unixtime(c2.create_time), "%Y-%m-%d") = "{1}") As n\
                    ON c1.customer_number = n.telephone_number\
                    WHERE date_format(from_unixtime(c1.start_time), "%Y-%m-%d") = "{2}"\
                        AND c1.status = "28"\
                    ) as j1\
                ON u.telephone_num = j1.t1\
                ) as j2\
        ON student_user_id = j2.t2\
        WHERE status NOT LIKE "CANCEL"\
            AND name NOT LIKE "测试%"\
            AND content NOT LIKE "测试%";').format(source, day_before_yesterday, yesterday)
cur.execute(sql)
result = cur.fetchall()

j = 0
for j in range(len(result)):
    e = 0
    b = list()
    for e in range(len(result[j])):
        b.append('JiShiFuDao')
        b.append('preorder created')
        b.append(result[j][e])
        print result[j][e],
    a.append(b)
    print len(a), 'rows done'
cur.close()
db.close()

# --- 写csv ---
yest_in_name = datetime.datetime.strftime(yesterday, '%m_%d')
datafile_name = 'new_incoming_%s.csv' % yest_in_name

with open(datafile_name, 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerows(a)


# --- 加附件，发邮件 ---
From = "zhijie.liu@lejent.com"  # 登陆邮箱
password = 'Woshijie123'  #登陆密码
To = "danping.li@lejent.com"  # 收件人邮箱

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
