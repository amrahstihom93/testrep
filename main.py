# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 12:52:09 2018

@author: MohitSharma
"""
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.factorplots import interaction_plot
import scipy.stats as stats
import matplotlib.pyplot as plt
from pandas.tools import plotting

df=pd.read_csv("data/ToothGrowth.csv")

fig=interaction_plot(df.dose, df.supp, df.len,
                     colors=['red','blue'],
                     markers=['D','^'],
                     ms=10)

N=len(df.len)

df_a = len(df.supp.unique()) - 1
df_b = len(df.dose.unique()) - 1
df_axb = df_a*df_b 
df_w = N - (len(df.supp.unique())*len(df.dose.unique()))

grand_mean = df['len'].mean

ssq_a = sum([(df[df.supp ==l].len.mean()-grand_mean)^2 for l in df.supp])
ssq_b = sum([(df[df.supp ==l].len.mean()-grand_mean)^2 for l in df.dose])

ssq_t = ((df.len-grand_mean)^2)

vc = df[df.supp == 'VC']
oc = df[df.supp == 'OJ']

vc_dose_means = [vc[vc.dose == d].len.mean() for d in vc.dose]
vc_dose_means = [oc[oc.dose == d].len.mean() for d in oc.dose]
ssq_w = sum((oc.len - oc_dose_means)^2) +sum((vc.len - vc_dose_means)^2)

ssq_axb = ssq_t-ssq_a-ssq_b-ssq_w

ms_a = ssq_a/df_a
ms_b = ssq_b/df_b

ms_axb = ssq_axb/df_axb
ms_w = ssq_w/df_w

f_a = ms_a/ms_w
f_b = ms_b/ms_w
f_axb = ms_axb/ms_w

p_a = stats.f.sf(f_a, df_a, df_w)
p_b = stats.f.sf(f_b, df_b, df_w)
p_axb = stats.f.sf(f_axb, df_axb, df_w)

results = {'sum_sq':[ssq_a, ssq_b, ssq_axb, ssq_w],
           'df':[df_a, df_b, df_axb, df_w],
           'F':[f_a, f_b, f_axb, 'NaN'],
            'PR(>F)':[p_a, p_b, p_axb, 'NaN']}
columns=['sum_sq', 'df', 'F', 'PR(>F)']

aov_table1 = pd.DataFrame(results, columns=columns,
                          index=['supp', 'dose', 
                          'supp:dose', 'Residual'])

def eta_squared(aov):
    aov['eta_sq'] = 'NaN'
    aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])
    return aov

def omega_squared(aov):
    mse = aov['sum_sq'][-1]/aov['df'][-1]
    aov['omega_sq'] = 'NaN'
    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*mse))/(sum(aov['sum_sq'])+mse)
    return aov


eta_squared(aov_table1)
omega_squared(aov_table1)
print(aov_table1)

