'''
https://poloniex.com/public?command=returnChartData&
currencyPair=BTC_XMR&
start=154630080&
end=1546646400&period=14400
'''
import requests 
from datetime import datetime
from datetime import timedelta

def get_data():
    end = datetime.now().timestamp()

    #YYYY-MM-DDTHH:MM:SS.mmmmmm
    #2018-03-10 00:00:00.000000
    #start_date=input()
    start_date='2020-05-17'
    start= datetime.strptime(start_date, '%Y-%m-%d').timestamp()
    #start=int(start.timestamp()*10**9)
    print("timestamp =", start)
    period=86400
    url="https://poloniex.com/public"
    data={'command':'returnChartData',
        'currencyPair':'BTC_XMR',
    'start': start,
    'end' : end,
    'period':period
    }
    BTC=requests.get(url, params= data).json()
    print(len(BTC))
    return BTC

def predict(data):
    prediction={}
    for i in range(len(data)):
        time=datetime.now()+timedelta(days=i)
        time=str(time.year)+"-"+str(time.month)+'-'+str(time.day)
        #time=i
        prediction[time]=data[i]['volume']
    return prediction

print(predict(get_data()))