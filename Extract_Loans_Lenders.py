import pandas as pd
import numpy as np
from datetime import date

pd.set_option('display.max_columns', None)
fields = ['LOAN_ID', 'POSTED_TIME']
loans = pd.read_csv('loans.csv', usecols = fields)
loans['POSTED_TIME'] = loans['POSTED_TIME'].astype('datetime64[ns]')
loans = loans[loans['POSTED_TIME'] > '2016-12-31']
loans = loans[loans['POSTED_TIME'] < '2018-01-01']
#loans.to_csv("loans_2017.csv")
loanslenders = pd.read_csv("loans_lenders.csv")
loanslenders = pd.merge(loans, loanslenders, on='LOAN_ID', how='outer')
loanslenders = loanslenders[loanslenders.POSTED_TIME.notnull()]
#print loanslenders.shape[0]

loanslenders = loanslenders.drop(['POSTED_TIME'], axis = 1)
loanslenders.to_csv("loanslenders_2017.csv")

# reshaped = \
# (loanslenders.set_index(loanslenders.columns.drop('LENDERS', 1).tolist())
#    .LENDERS.str.split(',', expand=True)
#    .stack()
#    .reset_index()
#    .rename(columns={0:'LENDERS'})
#    .loc[:, loanslenders.columns]
# )

# reshaped.to_csv("loanslenders_2017.csv")