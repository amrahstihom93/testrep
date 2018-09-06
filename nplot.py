import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.factorplots import interaction_plot
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np


datafile="data/Book1.csv"
data = pd.read_csv(datafile)

formula = 'Item ~ C(Units) + C(Region) + C(Units):C(Region)'
model = ols(formula, data).fit()
aov_table = anova_lm(model, typ=2)
 
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
df = aov_table.replace(np.nan, 0)
print(df)