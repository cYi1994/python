# -*- coding: utf-8 -*-

import pandas as pd

From = "chuan.yi@lejent.com"
To = "chuan.yi@lejent.com"
file_name1 = "7.6咨询师拨打日报.xls"
file_name2 = "email_test.xlsx"
df1 = pd.read_excel(file_name1, encoding='utf-8')
df2 = pd.read_excel(file_name2, encoding='utf-8')
print df1[u'咨询师姓名'][0]
print df2
#for i in range(len(df1)):
 #   for j in range(len(df2)):
  #      df1[u'咨询师姓名'][i] = df2['0'][j]
   #     print df2[1][j]



