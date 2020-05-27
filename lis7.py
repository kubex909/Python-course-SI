import random
import requests
from matplotlib.pyplot import *
from datetime import datetime,timedelta

def get_data():
    end = datetime.now().timestamp()
    start_date=input("Put date in format: YYYY-MM-DD \n")
    start= datetime.strptime(start_date, '%Y-%m-%d').timestamp()
    period=86400
    url="https://poloniex.com/public"
    data={'command':'returnChartData',
        'currencyPair':'BTC_XMR',
    'start': start,
    'end' : end,
    'period':period
    }
    BTC=requests.get(url, params= data).json()
    data=[]
    time=[]
    for i in BTC:
        data.append(i['volume'])
        time.append(i['date']) 
    return data,time

def analyse_data(data):
    lower=0
    min_diff_lower=max(data)-min(data)
    max_diff_lower=0
    min_diff_up=max(data)-min(data)
    max_diff_up=0
    for i in range(len(data)-1):
        if data[i]>data[i+1]:
            lower+=1
            if min_diff_lower>abs(data[i]-data[i+1]):
                min_diff_lower=abs(data[i]-data[i+1])
            if max_diff_lower<abs(data[i]-data[i+1]):
                max_diff_lower=abs(data[i]-data[i+1])
        else:
            if min_diff_up>abs(data[i]-data[i+1]):
                min_diff_up=abs(data[i]-data[i+1])
            if max_diff_up<abs(data[i]-data[i+1]):
                max_diff_up=abs(data[i]-data[i+1])
    max_diff_lower+=1
    max_diff_up+=1   
    probabilty=lower/len(data)
    new_data=[]
    new_data.append(data[-1])
    for i in range(0,len(data)):
        if random.choices([0,1],weights=[probabilty,1-probabilty])[0] ==0:
            new_data.append(new_data[i-1]-random.uniform(min_diff_lower,max_diff_lower))
        else: 
            new_data.append(new_data[i-1]+random.uniform(min_diff_up,max_diff_up))
    return new_data



time=[]
time2=[]
old_data,times=get_data()

#datetime.utcfromtimestamp(timedelta(days=1)).strftime('%Y-%m-%d')
#datetime.utcfromtimestamp(times[i]).strftime('%Y-%m-%d')
#time2.append(datetime.now)
for i in range(len(times)):
    time.append(datetime.utcfromtimestamp(times[i]).strftime('%m-%d'))
time2.append(time[-1])
for i in range(len(time)):
    time2.append((datetime.now()+timedelta(days=i)).strftime('%m-%d'))
#print(datetime.now())
#print(datetime.now()+timedelta(days=1))

average=[0]*(len(old_data)+1)
for i in range(100):
    print(i)
    new_data=analyse_data(old_data)
    for i in range(len(new_data)):
        average[i]+=new_data[i]
    #print(new_data)
    #print(average,"avg")
for i in range(len(average)):
    average[i]=average[i]/100   
plot(time,old_data,'b')
plot(time2,average,'r')
plot(time2,new_data,'g')
show()    
