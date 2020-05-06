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

    url='https://www.bitstamp.net/api/v2/transactions/bchusd/'
    BCH=requests.get(url,data=data).json()
    BCH,BCH_s=create_table(BCH)

    url='https://www.bitstamp.net/api/v2/transactions/xrpusd/'
    XRP=requests.get(url,data=data).json()
    XRP,XRP_s=create_table(XRP)

    url='https://www.bitstamp.net/api/v2/transactions/ltcusd/'
    LT=requests.get(url,data=data).json()
    LT,LT_s=create_table(LT)
    url='https://www.bitstamp.net/api/v2/transactions/ethusd/'
    ETH=requests.get(url,data=data).json()
    ETH,ETH_s=create_table(ETH)

    value=[BTC,BCH,XRP,LT,ETH]
    value2=[BTC_s,BCH_s,XRP_s,LT_s,ETH_s]
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
    return percent


def buy_sell_sum(money):  
    
    data,data2=bitbay()
    amount=[]
    price=[]
   
    
    for i in range(len(data)):
        amount.append([0,0,0,0])
        j=0
        while amount[i][0]<money and j<len(data[i]) and j<len(data2[i]):
            if  amount[i][0]+(data2[i][j][0]*data2[i][j][1])<money:
                amount[i][0]+=data2[i][j][0]*data2[i][j][1]
                amount[i][1]+=data2[i][j][1]
            else:   
                amount[i][1]+=(money-amount[i][0])/data2[i][j][0]
                amount[i][0]=money
            j+=1
        price.append(amount[i][0]/amount[i][1])
    

    for i in range(len(data)):
        j=-1
        amount[i][3]=amount[i][1]
        while amount[i][3]>0 and len(data2)+j>=0 and j+len(data)>=0:
            if  (amount[i][3]-data[i][j][1])>0:
                amount[i][2]+=data[i][j][0]*data[i][j][1]
                amount[i][3]-=data[i][j][1]
            else:   
                amount[i][2]+=amount[i][3]*data[i][j][0]
                amount[i][3]=0
            j-=1
        price[i]=round(((amount[i][2]/amount[i][1])/price[i]-1)*100,5)
    return price

def program(money):
    percent=buy_sell()
    percent2=buy_sell_sum(money)
    dictionary={percent[0]:'BTC',percent[1]:'BCH',percent[2]:'XRP',percent[3]:'LTC',percent[4]:'ETH'}
    percent=bubbleSort(percent,1)
    
    for i in range(len(percent)):
        print(dictionary[percent[i]], round(percent[i]*100,5),"%")

    dictionary2={percent2[0]:'BTC',percent2[1]:'BCH',percent2[2]:'XRP',percent2[3]:'LTC',percent2[4]:'ETH'}
    percent2=bubbleSort(percent2,1)
    print("value from second task with",money,"USD")
    for i in range(len(percent)):
        print(dictionary2[percent2[i]], percent2[i] ,"%")
    

while True:
    money=1000
    program(money)
    time.sleep(300)
    print("Refresh")
