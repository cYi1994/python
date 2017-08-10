
# -*- coding: utf-8 -*-

import pandas as pd
import MySQLdb
import datetime


db = MySQLdb.connect(host='10.44.62.51',
                     port=3308,
                     user='youzhangwei',
                     passwd='Aftyouzw4rjm',
                     db='afanti_online')
cur = db.cursor()

filepath = ("外呼公司邀约试听客户.xlsx")
df = pd.read_excel(filepath)

for i in range(df.__len__()):
    id = df[u'职员ID'][i]
    name = df[u'姓名'][i].encode('utf-8')
    team = df[u'小组'][i].encode('utf-8')
    group = df[u'大区'][i].encode('utf-8')
    tele = df[u'电话（11）'][i]
    email = df[u'企业邮箱'][i]
    title = df[u'岗位'][i].encode('utf-8')
    stime = datetime.datetime.strptime(df[u'入职时间'][i], '%m/%d/%Y')
    status = df[u'状态（在职，调岗，离职）'][i].encode('utf-8')


    insert_sql = 'INSERT INTO `sales_person_info` ' \
                 '(`sales_id`,`sales_name`,`sales_team`,`sales_group`,`telephone_num`,`enterprise_email`,`title`,`start_time`,`status`) \
                 VALUES ({0},"{1}","{2}","{3}",{4},"{5}","{6}",unix_timestamp("{7}"),"{8}")'.\
            format(id,name,team,group,tele,email,title,stime,status)
    print insert_sql
    cur.execute(insert_sql)

db.commit()
cur.close()
db.close()