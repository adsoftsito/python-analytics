import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
#from sklearn import datasets, linear_model

#from IPython.core.interactiveshell import InteractiveShell

#InteractiveShell.ast_node_interactivity = "all"

data=pd.read_csv("day.csv")
data.head()

import statsmodels.formula.api as smf

lm= smf.ols(formula= "cnt~weathersit", data=data).fit()
lm.params

lm.pvalues
print(lm.rsquared)
print(lm.rsquared_adj)

print(lm.summary())

