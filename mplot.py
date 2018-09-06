# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 10:50:09 2018

@author: MohitSharma
"""

import pandas as pd
import numpy as np
from scipy import stats

datafile="data/ToothGrowth.csv"
data = pd.read_csv(datafile)

#finding degrees of freedom
N = len(data.len)
df_a = len(data.supp.unique()) - 1
df_b = len(data.dose.unique()) - 1
df_axb = df_a*df_b 
df_w = N - (len(data.supp.unique())*len(data.dose.unique()))

#finding sum of squares
#finding grand_mean
grand_mean = data['len'].mean()

#finding SSa - supp
ssq_a = sum([(data[data.supp ==l].len.mean()-grand_mean)**2 for l in data.supp])

#finding SSb - dose
ssq_b = sum([(data[data.dose ==l].len.mean()-grand_mean)**2 for l in data.dose])

#finding SSt
ssq_t = sum((data.len - grand_mean)**2)

#finding SSwithin(error/residual)
vc = data[data.supp == 'VC']
oj = data[data.supp == 'OJ']
vc_dose_means = [vc[vc.dose == d].len.mean() for d in vc.dose]
oj_dose_means = [oj[oj.dose == d].len.mean() for d in oj.dose]
ssq_w = sum((oj.len-oj_dose_means)**2) + sum((vc.len-vc_dose_means)**2)

#finding sum of squares interaction
ssq_axb = ssq_t-ssq_a-ssq_b-ssq_w

#calculating mean squares
#finding mean square A
ms_a = ssq_a/df_a

#finding mean square B
ms_b = ssq_b/df_b

#finding mean square AXB
ms_axb = ssq_axb/df_axb

#finding mean square within/error/residual
ms_w = ssq_w/df_w
 

#f-ratio factors
f_a = ms_a/ms_w
f_b = ms_b/ms_w
f_axb = ms_axb/ms_w

# p-factor 
p_a = stats.f.sf(f_a, df_a, df_w)
p_b = stats.f.sf(f_b, df_b, df_w)
p_axb = stats.f.sf(f_axb, df_axb, df_w)


#sorting results into a table
results = {'sum_sq':[ssq_a, ssq_b, ssq_axb, ssq_w],
           'df':[df_a, df_b, df_axb, df_w],
           'F':[f_a, f_b, f_axb, 'NaN'],
           'PR(>F)':[p_a, p_b, p_axb, 'NaN'],
           }
columns=['sum_sq', 'df', 'F', 'PR(>F)']
 
aov_table = pd.DataFrame(results, 
                          columns=columns,
                          index=['supp', 
                                 'dose', 
                                 'supp:dose', 
                                 'Residual',
                                 ]
                          )

#finding eta and omega squares
def eta_squared(aov):
    aov['eta_sq'] = 'NaN'
    aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])
    return aov
 
def omega_squared(aov):
    mse = aov['sum_sq'][-1]/aov['df'][-1]
    aov['omega_sq'] = 'NaN'
    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*mse))/(sum(aov['sum_sq'])+mse)
    return aov
 
eta_squared(aov_table)
omega_squared(aov_table)

print(aov_table)