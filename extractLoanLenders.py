import pandas as pd
import numpy as np
from datetime import date

pd.set_option('display.max_columns', None)
fields = ['LOAN_ID', 'POSTED_TIME','SECTOR_NAME']
loans = pd.read_csv('loans.csv', usecols = fields)
loans['POSTED_TIME'] = loans['POSTED_TIME'].astype('datetime64[ns]')
loans = loans[loans['POSTED_TIME'] > '2016-12-31']
loans = loans[loans['POSTED_TIME'] < '2018-01-01']
loanslenders = pd.read_csv("loans_lenders.csv")
loanslenders = pd.merge(loans, loanslenders, on='LOAN_ID', how='outer')
loanslenders = loanslenders[loanslenders.POSTED_TIME.notnull()]
print loanslenders.shape[0]

loanslenders = loanslenders.drop(['POSTED_TIME'], axis = 1)
loanslenders.to_csv("loans_lenders_category_2017.csv")

