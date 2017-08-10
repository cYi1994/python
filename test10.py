#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import csv
import pandas as pd


filepath = "67试听未成单电话.xlsx"
df = pd.read_excel(filepath, names=['telephone_num'])


db = MySQLdb.connect(host='',
                     port=,
                     user='',
                     passwd='',
                     db='')

cur = db.cursor()
a = list()
for i in range(len(df['telephone_num'])):
    sql = "SELECT u.telephone_num, u.user_id \
            FROM user_online u\
            WHERE u.telephone_num = {0}".format(df['telephone_num'][i])
    cur.execute(sql)
    result = cur.fetchall()

    j = 0
    for j in range(len(result)):
        e = 0
        b = list()
        for e in range(len(result[j])):
            b.append(result[j][e])
        a.append(b)
    print b
    print len(a), 'rows done'

headers = ['telephone_num', 'user_id']
with open('67试听未成单id_tele.csv', 'wb') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(a)
