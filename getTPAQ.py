import urllib.request as request
import pandas as pd
import numpy as np
import datetime
import json

start = input('請輸入開始時間 (ex.2020-01-01) :')
end   = input('請輸入結束時間 (ex.2020-01-15) :')

stons = ['C0','C1','C10','C12','C13','C2','C3','C4','C5','C6','C7','C8','C9']

date = pd.date_range(start, end, freq='1d')
Date = [datetime.datetime.strftime(dd, '%Y-%m-%d') for dd in date]

Data = pd.DataFrame()

for DD in Date:
    src = 'https://eaqm-ap.taipower.com.tw/TPAQ/Webservice_SimEnvi/getData.aspx?Type=TPAQ&QueryTime=' + \
          DD + '&token=[EPA_TOKEN]'

    with request.urlopen(src) as response:
        results = json.load(response)

    column = ['SampleData', 'SiteID', 'PM25_AVG']

    for result in results:
        value = [result['SampleDate'], result['SiteID'], result['PM25_AVG']]
        for st in stons:
            if result['SiteID'] == st:
               data = pd.DataFrame(dict(zip(column, value)), \
                                   index= [DD + '-' + \
                                   result['SampleDate'][11:13]])
               Data = pd.concat([Data, data], axis = 0)


Data = Data.sort_values(by=['SiteID', 'SampleData'])
Data = Data.drop(['SampleData'], axis = 1)
Data = Data.replace(['9999',np.nan], -999)
Data = Data.set_index([Data.index, 'SiteID'])
Data = Data.unstack(1)

sts=[]
for col in Data.columns:
   pm,st = col
   sts.append(st)
Data.columns = sts

Data.to_csv('./Data/TPAQ(' + start + '_' + end + ')_avgPM25.csv')
print(Data)

    
