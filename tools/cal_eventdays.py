import pandas as pd
import os

start = input('請輸入開始時間 (ex.2020-01-01) :')
end   = input('請輸入結束時間 (ex.2020-01-15) :')
title = '('+start+'_'+end+')'
Times = pd.date_range(start, end, freq='1d').strftime('%Y-%m-%d')


inDir = os.path.join(os.getcwd(), '..', 'Data')
dataEPA = pd.read_csv(inDir+'/EPA'+title+'_avgPM25.csv', index_col=0)
dataTPAQ = pd.read_csv(inDir+'/TPAQ'+title+'_avgPM25.csv', index_col=0)
df = pd.concat([dataEPA, dataTPAQ], axis=1)
#df = df.drop(['三義', '苗栗'], axis=1)
df.index = [pd.to_datetime(dd) for dd in df.index]
print(df)


CountDf = pd.DataFrame(0, columns=df.columns, index=Times)
for date in Times:
    for st in df.columns:
        for vv in df.loc[date, st]:
            if vv > 35:
               CountDf.loc[date, st] += 1

CountDf['站時數'] = CountDf.sum(axis=1)
print(CountDf)
outDir = os.path.join(os.getcwd(), 'Output')
CountDf.to_csv(outDir+'/EventDays'+title+'.csv', encoding='utf-8-sig')
