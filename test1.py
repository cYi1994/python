
# -*- coding: utf-8 -*-

import MySQLdb

db = MySQLdb.connect(host='10.44.62.51',
                     port=3308,
                     user='youzhangwei',
                     passwd='Aftyouzw4rjm',
                     db='afanti_online')
cur = db.cursor()

def get_call_times(input_num):
    sql1 = "SELECT c1.customer_number, COUNT(c1.customer_number) \
            FROM crm_call_outcome_record c1 \
            WHERE c1.status <> 24 \
            AND c1.customer_number = {0} \
            GROUP BY c1.customer_number \
            HAVING COUNT(c1.customer_number) < 5 \
            ORDER BY COUNT(c1.customer_number)".format(input_num)

    cur.execute(sql1)
    a = {}
    for row in cur:
        a[int(row[0])] = int(row[1])
    print a

#get_call_times(15861575089)

def get_call_history(input_num):
    sql2 = "SELECT c1.customer_number,\
                    c1.client_name,\
                    c1.status,\
                    FROM_UNIXTIME(c1.start_time),\
                    SEC_TO_TIME(c1.total_duration)\
            FROM crm_call_outcome_record c1\
            WHERE c1.status <> 24 \
            AND c1.customer_number = {0}".format(input_num)
    cur.execute(sql2)
    a = {}
    for row in cur:
        if a.has_key(int(row[0])):
            a[int(row[0])].append((row[1],row[2],row[3],row[4]))
        else:
            a[int(row[0])] = [(row[1],row[2],row[3],row[4])]
    for kk in [' '.join([str(ee).strip() for ee in e]) for e in a.values()[0]]:
        print input_num, kk
get_call_history(13755966683)

#import csv
#with open('mycsvfile.csv', 'wb') as f:  # Just use 'w' mode in 3.x
#    a = get_call_history(13755966683)
#    w = csv.DictWriter(f, a.keys())
#    w.writeheader()
#    w.writerow(a)

#for kk in [' '.join([str(ee).strip() for ee in e]) for e in a.values()[0]]:
   # print kk