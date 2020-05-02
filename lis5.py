import time
import requests


def bitbay():
    BTC=requests.get('https://bitbay.net/API/Public/BTC/USD/ticker.json').json()
    BTC_b=BTC['bid']
    BTC=BTC['ask']
    ZEC=requests.get('https://bitbay.net/API/Public/ZEC/USD/ticker.json').json()
    ZEC_b=ZEC['bid']
    ZEC=ZEC['ask']
    ETH=requests.get('https://bitbay.net/API/Public/ETH/USD/ticker.json').json()
    ETH_b=ETH['bid']
    ETH=ETH['ask']
    LTC=requests.get('https://bitbay.net/API/Public/LTC/USD/ticker.json').json()
    LTC_b=LTC['bid']
    LTC=LTC['ask']
    DASH=requests.get('https://bitbay.net/API/Public/DASH/USD/ticker.json').json()
    DASH_b=DASH['bid']
    DASH=DASH['ask']
    value=[BTC,ZEC,ETH,LTC,DASH]
    value_bid=[BTC_b,ZEC_b,ETH_b,LTC_b,DASH_b]
    return value,value_bid

def bubbleSort(data,side):
    lenght=len(data)
    swapped= True    
    while (swapped == True):
        swapped= False
        if side ==0:
            for i in range(lenght-1):
                if data[i]>data[i+1]:
                    data[i], data[i+1] = data[i+1], data[i] 
                    swapped = True
        else:
            for i in range(lenght-1):
                if data[i]<data[i+1]:
                    data[i], data[i+1] = data[i+1], data[i] 
                    swapped = True

    return data

def buy_sell():
    data,data2=bitbay()
    percent=[]
    for i in range(len(data)):
        percent.append((data[i]-data2[i])/data[i])
        
    
    dictionary={percent[0]:'BTC',percent[1]:'ZEC',percent[2]:'ETH',percent[3]:'LTC',percent[4]:'DASH'}
    percent=bubbleSort(percent,1)
    
    for i in range(len(percent)):
        print(dictionary[percent[i]], round(percent[i]*100,2),"%")
    


while True:
    buy_sell()
    time.sleep(300)
    print("Refresh")
