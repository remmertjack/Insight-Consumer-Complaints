import pandas as pd
from datetime import datetime
pd.set_option('display.max_rows', 10)

data = pd.read_csv(input_file)
data['Date received']=pd.to_datetime(data['Date received'])
data['key'] = data['Product']+'--'+data['Date received'].dt.year.astype(str)

key_check = 'Credit reporting, credit repair services, or other personal consumer reports--2019'
data.loc[data['key']==key_check]

complaints['"credit reporting, credit repair services, or other personal consumer reports"--2019']
data['value_'] = 1

p_count = data.groupby('key')['Company'].count()

# unique
p_unique = data.groupby('key')['Company'].agg(['nunique']).reset_index()
p_unique.loc[p_unique['key']=='Virtual currency--2017']

p_unique.loc[ p_unique['nunique'] <=50 ]
# mx
check = data.loc[data['key']=='Prepaid card--2014']
vc = check['Company'].value_counts()
check.loc[check['Company']== 'AMERICAN EXPRESS COMPANY']

complaints['Credit card or prepaid card--2020']
sum(vc)

p_mx = data.groupby('key')['Company'].value_counts().max(level=0)

p_count.to_csv('count.csv',index=True)
p_unique.to_csv('unique.csv',index=True)
p_mx.to_csv('mx.csv',index=True)

key_check = 'Debt collection--2020'
data.loc[data['key']==key_check].to_csv('check_db.csv',index=False)

p_count = pd.DataFrame(p_count).reset_index(False)
p_unique.loc[p_unique['key']==key_check]
#p_unique = pd.DataFrame(p_unique).reset_index(True)
p_mx = pd.DataFrame(p_mx).reset_index(False)
p_mx.columns = ['key','mx']

mg_p = p_count.merge(pd.DataFrame(p_unique), how = 'left', on ='key')
mg_p= mg_p.merge(pd.DataFrame(p_mx), how = 'left', on ='key')
mg_p.to_csv('count2.csv',index=True)
