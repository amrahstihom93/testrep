# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 15:59:30 2018

@author: MohitSharma
"""


import pandas as pd
from scipy import stats
import numpy as np

datafile = "data/Book1.csv"
data = pd.read_csv(datafile)

c = data.columns
print (c)
#prints data
#print(data)
#grpd=data.groupby('Region')
#print (grpd)
#data plot
#data.boxplot('Unit Cost', by='Region')

#grps = pd.unique(data.group.values)
#d_data = {grp:data['weight'][data.group==grp] for grp in grps}

k=len(pd.unique(data.Region))
print(k)
N=len(data.values)
print(N)
n=data.groupby('Region').size()[0]
print(n)

#one-way ANOVA
#f,p=stats.f_oneway(d_data['ctrl'],d_data['trt1'], d_data['trt2'])

#print(f, p)

g_mean = sum(data['Units'].values)/N
print("gmean==>", g_mean)
print("sum of cells")

#calculating sst
#val-g_mean
sst = (data['Units'].iloc[range(N)]-g_mean)
print("sst", sst)
#print("DATA units sum ", data['Units'].sum())
ss_between = (sum(data.groupby('Region').sum()['Units']**2)/n) - (data['Units'].sum()**2)/N

print(sum(data['Units'].values))
sum_y_squared = sum([value**2 for value in data['Units'].values])
ss_within = sum_y_squared - sum(data.groupby('Region').sum()['Units']**2)/n
ss_total = sum_y_squared - (data['Units'].sum()**2)/N

#print(sum(data.groupby('Region').sum()['Units']**2))
#print(data['Units'].sum()**2)
print(ss_between)
#degrees of freedom
df_between = k-1
df_within = N-k
df_total = df_between + df_within

print(df_between)
print(df_within)
print(df_total)
#mean square
ms_between = ss_between/df_between
ms_within = ss_within/df_within

#calculating the f-ration
f = ms_between/ms_within

#calculating p-value
p=stats.f.sf(f, df_between, df_within)

#effect sizes
eta_squared = ss_between/ss_total
omega_squared = (ss_between - (df_between * ms_within))/(ss_total + ms_within)

results = {'f':[f],
           'p':[p],
           'eta':[eta_squared],
           'omega':[omega_squared],
           }
columns=['f', 'p', 'eta', 'omega']
 
aov_table = pd.DataFrame(results, 
                          columns=columns,
                          index=['']
                          )

print(aov_table)
