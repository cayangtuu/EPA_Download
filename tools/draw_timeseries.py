import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

date = ['2020-11-01', '2020-11-30']
date_list = [dt.datetime.strptime(date[0],'%Y-%m-%d'), 
             dt.datetime.strptime(date[1],'%Y-%m-%d') + dt.timedelta(days=1)]
dateRange = [dd.date() for dd in date_list]


indir = os.path.join(os.getcwd(), '..', 'Data')
dataEPA  = pd.read_csv(indir+'EPA(' + date[0] + '_' + date[1] + ')_avgPM25.csv',
                       index_col=0, encoding='utf-8-sig')
dataEPA = dataEPA.replace(-999, np.nan)

dataTPAQ = pd.read_csv(indir+'TPAQ(' + date[0] + '_' + date[1]  + ')_avgPM25.csv', 
                        index_col=0, encoding='utf-8-sig')
dataTPAQ = dataTPAQ.replace(-999, np.nan)

data = dataEPA.join(dataTPAQ, how='outer')
data.index = pd.date_range(date_list[0], date_list[1] - dt.timedelta(hours=1), freq='1h')
#data = data.resample('D').mean()
data['Mean'] = round(data.mean(axis=1, skipna=True),2)
print(data)

# Draw Timeseries
outdir = './Output_timeseries/'
#picFil = outdir + 'output_days(' + date[0] + '_' + date[1] + ')'
picFil = outdir + 'output_hrs(' + date[0] + '_' + date[1] + ')'
fig, ax = plt.subplots(figsize = (20 , 3))
ax.plot(data.index, data['Mean'], label='PM2.5_AVG', color='k', linestyle='-')
ax.set_xlim(dateRange)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
ax.xaxis.set_ticks(np.arange(np.datetime64(dateRange[0]),
                             np.datetime64(dateRange[1]), 
                             np.timedelta64(1, 'D')))
plt.xticks(rotation=45, fontsize=10)
ax.set_ylabel('PM2.5_AVG(ug/m^3)', fontsize=10)
ax.set_title('Timeseries of Average PM2.5 in November')
ax.grid(True)

plt.tight_layout()
plt.savefig(picFil)
plt.close()
