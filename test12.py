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
yest_in_name = datetime.datetime.strftime(yesterday, '%m_%d')
datafile_name1 = 'tianrun_outcome_%s.csv' % yest_in_name
datafile_name2 = 'create_preorder_sales_%s.csv' % yest_in_name
datafile_name3 = 'start_preorder_sales_%s.csv' % yest_in_name
datafile_name4 = 'finished_preorder_sales_%s.csv' % yest_in_name
datafile_name5 = 'series_order_%s.csv' % yest_in_name

# --- 加附件，发邮件 ---
From = "chuan.yi@lejent.com"  # 登陆邮箱
To = "chuan.yi@lejent.com"  # 收件人邮箱
password = ''

server = smtplib.SMTP("smtp.exmail.qq.com")
server.login(From, "password")  # 仅smtp服务器需要验证时

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
