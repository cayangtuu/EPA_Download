import urllib.request as request
import pandas as pd
import numpy as np
import datetime
import json

start = input('請輸入開始時間 (ex.2020-01-01) :')
end   = input('請輸入結束時間 (ex.2020-01-15) :')

stons = ['二林','南投','埔里','大里','彰化','忠明','沙鹿','竹山','線西','西屯','豐原']

date = pd.date_range(start, end, freq='1d')
Date = [datetime.datetime.strftime(dd, '%Y-%m-%d') for dd in date]

Data = pd.DataFrame()

for DD in Date:
    src = 'https://eaqm-ap.taipower.com.tw/TPAQ/Webservice_SimEnvi/getData.aspx?Type=EPA&QueryTime=' + \
          DD + '&token=[EPA_TOKEN]' 

    with request.urlopen(src) as response:
        results = json.load(response)

    column = ['PublishTime', 'SiteName', 'PM25_AVG']

    for result in results:
        value = [result['PublishTime'], result['SiteName'], result['PM2.5_AVG']]
        for st in stons:
            if result['SiteName'] == st:
               data = pd.DataFrame(dict(zip(column, value)), \
                                   index= [DD + '-' + \
                                   result['PublishTime'][11:13]])
               Data = pd.concat([Data, data], axis = 0)


Data = Data.sort_values(by=['SiteName', 'PublishTime'])
Data = Data.drop(['PublishTime'], axis = 1)
Data = Data.replace(['', np.nan], -999)
Data = Data.set_index([Data.index, 'SiteName'])
Data = Data.unstack(1)

sts=[]
for col in Data.columns:
   pm,st = col
   sts.append(st)
Data.columns = sts

Data.to_csv('./Data/EPA(' + start + '_' + end + ')_avgPM25.csv', encoding = 'utf-8-sig')
print(Data)

    
