import time
import requests
import operator

def create_table(tab):
    data=[]
    data2=[]
    for i in range(len(tab)):
        data_p=tab[:][i]['price']
        data_t=tab[:][i]['type']
        data_a=tab[:][i]['amount']
        if data_t=="0":
            data.append([float(data_p),float(data_a)])
        else:
            data2.append([float(data_p),float(data_a)])
    data=bubbleSort(data,0)
    return data,data2


def bitbay():
    url='https://www.bitstamp.net/api/v2/transactions/btcusd/'
    data={'time':'day'}
    BTC=requests.get(url, data= data).json()
    BTC,BTC_s=create_table(BTC)

    url='https://www.bitstamp.net/api/v2/transactions/eurusd/'
    EURO=requests.get(url,data=data).json()
    EURO,EURO_s=create_table(EURO)

    url='https://www.bitstamp.net/api/v2/transactions/xrpusd/'
    XRP=requests.get(url,data=data).json()
    XRP,XRP_s=create_table(XRP)

    url='https://www.bitstamp.net/api/v2/transactions/ltcusd/'
    LT=requests.get(url,data=data).json()
    LT,LT_s=create_table(LT)
    url='https://www.bitstamp.net/api/v2/transactions/ethusd/'
    ETH=requests.get(url,data=data).json()
    ETH,ETH_s=create_table(ETH)

    value=[BTC,EURO,XRP,LT,ETH]
    value2=[BTC_s,EURO_s,XRP_s,LT_s,ETH_s]
    return value,value2

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
        percent.append((data[i][-1][0]/data2[i][0][0])-1)
            
    dictionary={percent[0]:'BTC',percent[1]:'EUR',percent[2]:'XRP',percent[3]:'LTC',percent[4]:'ETH'}
    percent=bubbleSort(percent,1)
    
    for i in range(len(percent)):
        print(dictionary[percent[i]], round(percent[i]*100,2),"%")
    


while True:
    buy_sell()
    time.sleep(300)
    print("Refresh")
