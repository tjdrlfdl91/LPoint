# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 19:03:33 2018

@author: SKMOON
"""

cwd = "D:/Downloads/DigitalTrendAnalyzer" #skmoon (PC)

import os
os.getcwd()
os.chdir(cwd)

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df01 = pd.read_csv("01.Product.csv")
df02 = pd.read_csv("02.Search1.csv")
df03 = pd.read_csv("03.Search2.csv")
df04 = pd.read_csv("04.Custom.csv")
df05 = pd.read_csv("05.Session.csv")
df06 = pd.read_csv("06.Master.csv")

df01.head()
df02.head()
df03.head()
df04.head()
df05.head()
df06.head()


### 우선 제일 만만한 매크로 검색량 데이터 'df03'부터 건드려봅시다
df03.dtypes

# 검색량이 object로 돼있으므로 숫자로 바꿔줍니다
df03['SEARCH_CNT'] = df03['SEARCH_CNT'].convert_objects(convert_numeric=True)

# 일자 별로 검색량의 변화를 살펴볼 수 있습니다
df03.sort_values(by = ['SEARCH_CNT'], ascending=False).head(20) # 전체 검색량 순위
df03.loc[(df03['SEARCH_CNT'] >= 100) & (df03['SEARCH_CNT'] < 150.0)].head(20) #100개 이상 150개 미만에 해당하는 검색어들
df03.loc[df03['KWD_NM'] == '뉴발란스운동화'].sort_values(by = ['SESS_DT']) #일자별 뉴발란스 운동화 검색량 추이

date_raw = df03.loc[df03['KWD_NM'] == '뉴발란스운동화'].sort_values(by = ['SESS_DT'])['SESS_DT']
date_modified = date_raw.apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
count_newbal = df03.loc[df03['KWD_NM'] == '뉴발란스운동화'].sort_values(by = ['SESS_DT'])['SEARCH_CNT']
count_adidas = df03.loc[df03['KWD_NM'] == '아디다스운동화'].sort_values(by = ['SESS_DT'])['SEARCH_CNT']
count_nike = df03.loc[df03['KWD_NM'] == '나이키운동화'].sort_values(by = ['SESS_DT'])['SEARCH_CNT']

plt.plot(date_modified, count_newbal, color = 'gray')
plt.plot(date_modified, count_adidas, color = 'black')
plt.plot(date_modified, count_nike, color = 'orange')
plt.xlabel('Date')
plt.ylabel('Search Counts')
plt.title('Shoes Search Counts')
plt.legend(['NewBal', 'Adidas', 'Nike'])
plt.show() #일자별 운동화 검색량 비교 시각화

# 특정 키워드를 포함한 검색어의 추이도 살펴볼 수 있습니다
search_word = df03.loc[df03['KWD_NM'].str.contains('미세먼지')] #미세먼지 키워드를 포함한 검색어의 검색량 추이
search_word = search_word.groupby('SESS_DT').sum() #일자별로 묶음
len(search_word) #183일 중 158일만 미세먼지에 대해 검색함

search_word = search_word.reset_index()

date = date_raw.reset_index()
date.drop('index', axis = 1, inplace = True) #전체 분석기간

search = pd.merge(date, search_word, on = 'SESS_DT', how = 'outer')
search.fillna(0, inplace = True) #검색량이 없는 날에는 0으로 채움

search['SESS_DT'] = search['SESS_DT'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

plt.plot(search['SESS_DT'], search['SEARCH_CNT'])
plt.xlabel('Date')
plt.ylabel('Search Counts')
plt.title('Fine Dust Search Counts')
plt.legend(['Fine Dust'])
plt.show() #일자별 미세먼지 키워드를 포함한 검색어의 검색량 시각화



### 품목별 매출액 규모를 알아봅시다
### 제품, 대분류, 중분류, 소분류 별로 알아볼 수 있습니다
sales = df01.drop(['PD_ADD_NM', 'PD_BRA_NM'], axis = 1)
sales['REV'] = sales['PD_BUY_AM'] * sales['PD_BUY_CT'] #매출액 계산

sales_by_product = sales.groupby('PD_C').sum()
sales_by_class1 = sales.groupby('CLAC1_NM').sum()
sales_by_class2 = sales.groupby('CLAC2_NM').sum()
sales_by_class3 = sales.groupby('CLAC3_NM').sum()

sales_by_product = sales_by_product.reset_index()
sales_by_product = pd.merge(sales_by_product, df06, on = 'PD_C', how = 'inner')
sales_by_product.sort_values(by = ['REV'], ascending = False).head(20)

sales_by_class1 = sales_by_class1.reset_index()
sales_by_class1.sort_values(by = ['REV'], ascending = False).head(20)

sales_by_class2 = sales_by_class2.reset_index()
sales_by_class2.sort_values(by = ['REV'], ascending = False).head(20)

sales_by_class3 = sales_by_class3.reset_index()
sales_by_class3.sort_values(by = ['REV'], ascending = False).head(20)





### 작업 중 (무시하세요)


df01['PD_BUY_AM'] = df01['PD_BUY_AM'].map(lambda row: row.replace(',', ''))
df01['PD_BUY_CT'] = df01['PD_BUY_CT'].convert_objects(convert_numeric=True)
df01['PD_BUY_AM'] = df01['PD_BUY_AM'].convert_objects(convert_numeric=True)
df01['REV'] = df01['PD_BUY_AM'] * df01['PD_BUY_CT']

df01.sort_values(by=['HITS_SEQ']).head()

temp01 = df01.loc[df01.CLNT_ID == [1738139]].sort_values(by=['SESS_ID', 'HITS_SEQ'])

df02.loc[df02.CLNT_ID == [1738139]]
df02.loc[df02.CLNT_ID == [1738139]].sort_values(by=['SESS_ID']) 

df04.loc[df04.CLNT_ID == [1738139]] ## 40대 남성

temp05 = df05.loc[df05.CLNT_ID == [1738139]].sort_values(by=['SESS_SEQ'])

pd.merge(temp01, temp05, on = 'SESS_ID', how = 'inner').sort_values(by=['SESS_SEQ', 'HITS_SEQ'])



df03.loc[df03['SEARCH_CNT'] > 100].head()