import random
import requests
from matplotlib.pyplot import *
from datetime import datetime,timedelta

def get_data(start_date, currencypair, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d').timestamp()
    end= datetime.strptime(end_date, '%Y-%m-%d').timestamp()
    period=86400
    url="https://poloniex.com/public"
    data={'command':'returnChartData',
        'currencyPair':currencypair,
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

    return min_diff_lower,max_diff_lower,min_diff_up,max_diff_up,probabilty

def generate_data(data,min_diff_lower,max_diff_lower,min_diff_up,max_diff_up,probabilty):
    new_data=[]
    new_data.append(data[-1])
    for i in range(1,len(data)+1):
        if random.choices([0,1],weights=[probabilty,1-probabilty])[0] ==0:
            new_data.append(new_data[i-1]-random.uniform(min_diff_lower,max_diff_lower))
        else: 
            new_data.append(new_data[i-1]+random.uniform(min_diff_up,max_diff_up))
    return new_data

def select_cur():    
    print("1 - BTC-DASH")
    print("2 - BTC-ETH")
    print("3 - USDC-ETH")
    idpair=input("Chose currency pair: ")
    switcher={
        "1":"BTC_DASH",
        "2":"BTC_ETH",
        "3":"USDC_ETH",
    }
    correct_data=False
    while correct_data == False:

        pair=switcher.get(idpair)
        print("Chose your starting data, more then 1 year before would take more time to show results")
        #start_date=input("Put date in format: YYYY-MM-DD \n")
        start_date="2019-01-01"
        end_date="2019-06-01"
        if datetime.strptime(start_date, '%Y-%m-%d').timestamp() < datetime.now().timestamp():
            correct_data=True
        else:
            print("Enter historical data")
    return start_date,pair,end_date

def generate_time(times):
    time=[]
    time2=[]
    for i in range(len(times)):
        time.append(datetime.utcfromtimestamp(times[i]).strftime('%y-%m-%d'))
    time2.append(time[-1])
    for i in range(len(time)):
        time2.append((datetime.now()+timedelta(days=i+1)).strftime('%y-%m-%d'))
    return time,time2

def plots(time,old_data,time2,real_data):
    average=[0]*(len(old_data)+1)
    min_diff_lower,max_diff_lower,min_diff_up,max_diff_up,probabilty =analyse_data(old_data)
    for i in range(100):
        print(i)
        new_data=generate_data(old_data,min_diff_lower,max_diff_lower,min_diff_up,max_diff_up,probabilty)
        for i in range(len(new_data)):
            average[i]+=new_data[i]
    for i in range(len(average)):
        average[i]=average[i]/100   
    diference_with_1=[]
    diference_with_100=[]
    single_more=0
    multiple_more=0
    for i in range(len(average)):
        diference_with_1.append(abs(real_data[i]-average[i]))
        diference_with_100.append(abs(real_data[i]-new_data[i]))
    for i in range(len(diference_with_1)):
        if diference_with_1<diference_with_100:
            single_more+=1
        else:
            multiple_more+=1
    print(single_more,multiple_more)
    plot(time,old_data,'b')
    plot(time2,average,'r')
    plot(time2,new_data,'g')
    plot(time2,real_data)
    show()    
    plot(time2,diference_with_1,'b')
    plot(time2,diference_with_100,'r')
    show()

start_data,pair,end_data=select_cur()
old_data,times=get_data(start_data,pair,end_data)
real_data,tim=get_data(end_data,pair,"2019-10-31")
time,time2=generate_time(times)
plots(time,old_data,time2,real_data)


