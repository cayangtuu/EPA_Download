import pandas as pd
import os
start = '2022-01-01'
end = '2022-12-31'
dataDir = os.path.join(os.getcwd(), 'Data')
dateFirst = pd.date_range(start, end, freq='1MS').strftime('%Y-%m-%d')
dateEnd = pd.date_range(start, end, freq='1M').strftime('%Y-%m-%d')
dataDir = os.path.join(os.getcwd(), 'Data')

df = pd.DataFrame()
for ii in range(len(dateFirst)):
    date = dateFirst[ii]+'_'+dateEnd[ii]
    data = pd.read_csv(dataDir+'/TPAQ('+date+')_avgPM25.csv', encoding='utf-8-sig', index_col=0)
    df = pd.concat([df, data], axis=0)
print(df)
df.to_csv(dataDir+'/TPAQ('+start+'_'+end+')_avgPM25.csv', encoding='utf-8-sig')
