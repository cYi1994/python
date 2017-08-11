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


# --- database connection如有问题请联系林清 ---
# --- 发件人收件人可修改，改发件人别忘了改密码 ---

# --- app-0yst ---
# 1 --- 未拨出 ---
a = list()


def danping_weekly(source):

    db = MySQLdb.connect(host='',
                         port=,
                         user='',
                         passwd='',
                         db='')

    cur = db.cursor()
    sql = ('SELECT count(distinct c2.telephone_number) as "未拨出"\
            FROM crm_form_record c2\
            WHERE	(c2.source LIKE "{0}")\
                AND c2.telephone_number NOT IN\
                                            (\
                                            SELECT DISTINCT c1.customer_number\
                                            FROM crm_call_outcome_record c1\
                                            INNER JOIN (SELECT distinct (c2.telephone_number) as t\
                                                        FROM crm_form_record c2\
                                                        WHERE (c2.source LIKE "{0}")) As n\
                                            ON c1.customer_number = n.t\
                                            );').format(source)
    cur.execute(sql)
    result = cur.fetchall()


    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('not dialed')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # 2 --- 拨出 ---
    cur = db.cursor()
    sql = ('SELECT count(DISTINCT c1.customer_number) as "拨出"\
            FROM crm_call_outcome_record c1\
            INNER JOIN (SELECT distinct (c2.telephone_number) as t\
                        FROM crm_form_record c2\
                        WHERE c2.source LIKE "{0}") As n\
                        ON c1.customer_number = n.t;').format(source)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('dialed')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # 3 --- 接通去重 ---
    cur = db.cursor()
    sql = ('SELECT COUNT(distinct c3.customer_number) as "28去重"\
            FROM crm_call_outcome_record c3\
            JOIN (\
                SELECT DISTINCT c1.customer_number\
                FROM crm_call_outcome_record c1\
                INNER JOIN (SELECT distinct (c2.telephone_number) as t\
                            FROM crm_form_record c2\
                            WHERE c2.source LIKE "{0}") As n\
                ON c1.customer_number = n.t\
                ) as j\
            ON j.customer_number = c3.customer_number\
            WHERE c3.status = 28;').format(source)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('28 unique')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()
    # 4 --- 客户未接通数 ---
    cur = db.cursor()
    sql = ('SELECT COUNT(c3.customer_number) as "21"\
            FROM crm_call_outcome_record c3\
            JOIN (\
                    SELECT DISTINCT c1.customer_number\
                    FROM crm_call_outcome_record c1\
                    INNER JOIN (SELECT distinct (c2.telephone_number) as t\
                                FROM crm_form_record c2\
                                WHERE c2.source LIKE "{0}") As n\
                    ON c1.customer_number = n.t\
                    ) as j\
            ON j.customer_number = c3.customer_number\
            WHERE c3.status = 21;').format(source)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('21 unanswered')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # 5 --- 无效数 ---
    cur = db.cursor()
    sql = ('SELECT COUNT(c3.customer_number) as "22"\
            FROM crm_call_outcome_record c3\
            JOIN (\
                    SELECT DISTINCT c1.customer_number\
                    FROM crm_call_outcome_record c1\
                    INNER JOIN (SELECT distinct (c2.telephone_number) as t\
                                FROM crm_form_record c2\
                                WHERE c2.source LIKE "{0}") As n\
                    ON c1.customer_number = n.t\
                    ) as j\
            ON j.customer_number = c3.customer_number\
            WHERE c3.status = 22;').format(source)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('22 invalid')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()
    # 6 --- 座席未接通数 ---
    cur = db.cursor()
    sql = ('SELECT COUNT(c3.customer_number) as "24"\
            FROM crm_call_outcome_record c3\
            JOIN (\
                    SELECT DISTINCT c1.customer_number\
                    FROM crm_call_outcome_record c1\
                    INNER JOIN (SELECT distinct (c2.telephone_number) as t\
                                FROM crm_form_record c2\
                                WHERE c2.source LIKE "{0}") As n\
                    ON c1.customer_number = n.t\
                    ) as j\
            ON j.customer_number = c3.customer_number\
            WHERE c3.status = 24;').format(source)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('24 sales unanswered')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # 7 --- 接通数 ---
    cur = db.cursor()
    sql = ('SELECT COUNT(c3.customer_number) as "28"\
            FROM crm_call_outcome_record c3\
            JOIN (\
                    SELECT DISTINCT c1.customer_number\
                    FROM crm_call_outcome_record c1\
                    INNER JOIN (SELECT distinct (c2.telephone_number) as t\
                                FROM crm_form_record c2\
                                WHERE c2.source LIKE "{0}") As n\
                    ON c1.customer_number = n.t\
                    ) as j\
            ON j.customer_number = c3.customer_number\
            WHERE c3.status = 28;').format(source)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('28 talked')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # 8 --- 渠道试听邀约数 ---
    cur = db.cursor()
    sql = ('SELECT COUNT(pid) AS "渠道试听邀约数"\
            FROM tutor_preorder\
            JOIN (\
                    SELECT (u.user_id) as t2\
                    FROM user_online u\
                    JOIN\
                        (\
                        SELECT (c3.customer_number) t1\
                        FROM crm_call_outcome_record c3\
                        JOIN (\
                                SELECT DISTINCT c1.customer_number\
                                FROM crm_call_outcome_record c1\
                                INNER JOIN (SELECT distinct (c2.telephone_number) as t\
                                            FROM crm_form_record c2\
                                            WHERE c2.source LIKE "{0}") As n\
                                ON c1.customer_number = n.t\
                                ) as j\
                        ON j.customer_number = c3.customer_number\
                        WHERE c3.status = 28\
                        ) as j1\
                ON u.telephone_num = j1.t1\
                ) as j2\
            ON student_user_id = j2.t2\
            WHERE status = "BOOK"\
                AND category = "DEMO"\
                AND name NOT LIKE "%测试%"\
                AND content NOT LIKE "%测试%";').format(source)
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

    # 9 --- 渠道试听完成数 ---
    cur = db.cursor()
    sql = ('SELECT COUNT(DISTINCT p.pid) AS "渠道试听完成数"\
            FROM tutor_preorder p\
            JOIN (\
                    SELECT (u.user_id) as t2\
                    FROM user_online u\
                    JOIN\
                    (\
                        SELECT (c3.customer_number) t1\
                        FROM crm_call_outcome_record c3\
                        JOIN (\
                                SELECT DISTINCT c1.customer_number\
                                FROM crm_call_outcome_record c1\
                                INNER JOIN (SELECT distinct (c2.telephone_number) as t\
                                            FROM crm_form_record c2\
                                            WHERE c2.source LIKE "{0}") As n\
                                ON c1.customer_number = n.t\
                                ) as j\
                        ON j.customer_number = c3.customer_number\
                        WHERE c3.status = 28\
                        ) as j1\
                    ON u.telephone_num = j1.t1\
                    ) as j2\
            ON p.student_user_id = j2.t2\
            LEFT JOIN audio_record_info a ON p.tutor_record_id = a.tutor_record_id\
            WHERE p.status = "BOOK"\
                AND p.category = "DEMO"\
                AND p.name NOT LIKE "%测试%"\
                AND p.content NOT LIKE "%测试%"\
                AND p.tutor_record_id = a.tutor_record_id\
                AND from_unixtime(floor(a.start_time/1000)) IS NOT NULL\
                AND round((a.end_time-a.start_time)/60000) > 15;').format(source)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('preorder finished')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()

    # 10 --- 成单数和总金额 ---
    cur = db.cursor()
    sql = ('SELECT count(j3.pid) as "order #", sum(j3.amount/100) as "total amount"\
            FROM\
            (\
            SELECT distinct *\
            FROM series_order o\
            JOIN (\
                    SELECT (u.user_id) as t2\
                    FROM user_online u\
                    JOIN\
                    (\
                        SELECT (c3.customer_number) t1\
                        FROM crm_call_outcome_record c3\
                        JOIN (\
                                SELECT DISTINCT c1.customer_number\
                                FROM crm_call_outcome_record c1\
                                INNER JOIN (SELECT distinct (c2.telephone_number) as t\
                                            FROM crm_form_record c2\
                                            WHERE c2.source LIKE "{0}") As n\
                                ON c1.customer_number = n.t\
                                ) as j\
                        ON j.customer_number = c3.customer_number\
                        WHERE c3.status = 28\
                        ) as j1\
                    ON u.telephone_num = j1.t1\
                ) as j2\
            ON o.student_user_id = j2.t2\
            WHERE o.status = "SUCCESS"\
                AND o.amount > 10\
            ) as j3;').format(source)
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(source)
            b.append('orders and total amount')
            b.append(result[j][e])
            print result[j][e],
        a.append(b)
        print len(a), 'rows done'
    cur.close()
    db.close()

# source = '%zhjz%'
# print source
# danping_weekly(source)
# source = '%afanty100%'
# print source
# danping_weekly(source)
# source = '%jyjz%'
# print source
# danping_weekly(source)
# source = '%shequn%'
# print source
# danping_weekly(source)
# source = '%外呼%'
# print source
# danping_weekly(source)
source = '%app-|app_|APP-|APP_%'
print source
danping_weekly(source)
# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
# -------------------------------------------
# --- database connection如有问题请联系林清 ---
# --- 发件人收件人可修改，改发件人别忘了改密码 ---



# --- 写csv ---
yest_in_name = datetime.datetime.strftime(yesterday, '%m_%d')
datafile_name = 'weekly_source_update_%s.csv' % yest_in_name

with open(datafile_name, 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerows(a)


# --- 加附件，发邮件 ---
From = ""  # 登陆邮箱
password = ''  #登陆密码
To = ""  # 收件人邮箱

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
