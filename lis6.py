import time
import requests
import operator
import sqlite3
import csv
import sys

def create_table(tab,mode):
    data=[]
    data2=[]
    for i in range(len(tab)):
        data_p=tab[:][i]['price']
        data_t=tab[:][i]['type']
        data_a=tab[:][i]['amount']
        data_d=tab[:][i]['date']

        if data_t=="0":
            data.append([int(data_d),float(data_p),float(data_a)])
        else:
            data2.append([int(data_d),float(data_p),float(data_a)])
    data=bubbleSort(data,0)
    data2=bubbleSort(data2,0)
    return data,data2


def bitbay():
    url='https://www.bitstamp.net/api/v2/transactions/btcusd/'
    data={'time':'day'}
    BTC=requests.get(url, data= data).json()
    BTC,BTC_s=create_table(BTC,1)

    url='https://www.bitstamp.net/api/v2/transactions/bchusd/'
    BCH=requests.get(url,data=data).json()
    BCH,BCH_s=create_table(BCH,1)

    url='https://www.bitstamp.net/api/v2/transactions/xrpusd/'
    XRP=requests.get(url,data=data).json()
    XRP,XRP_s=create_table(XRP,1)

    url='https://www.bitstamp.net/api/v2/transactions/ltcusd/'
    LT=requests.get(url,data=data).json()
    LT,LT_s=create_table(LT,1)
    
    url='https://www.bitstamp.net/api/v2/transactions/ethusd/'
    ETH=requests.get(url,data=data).json()
    ETH,ETH_s=create_table(ETH,1)

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
        percent.append((data[i][-1][1]/data2[i][0][1])-1)
    return percent


def buy_sell_sum(money):  
    
    data,data2=bitbay()
    amount=[]
    price=[]
   
    
    for i in range(len(data)):
        amount.append([0,0,0,0])
        j=0
        while amount[i][0]<money and j<len(data[i]) and j<len(data2[i]):
            if  amount[i][0]+(data2[i][j][1]*data2[i][j][2])<money:
                amount[i][0]+=data2[i][j][1]*data2[i][j][2]
                amount[i][1]+=data2[i][j][2]
            else:   
                amount[i][1]+=(money-amount[i][0])/data2[i][j][1]
                amount[i][0]=money
            j+=1
        price.append(amount[i][0]/amount[i][1])
    

    for i in range(len(data)):
        j=-1
        amount[i][3]=amount[i][1]
        while amount[i][3]>0 and len(data2)+j>=0 and j+len(data)>=0:
            if  (amount[i][3]-data[i][j][2])>0:
                amount[i][2]+=data[i][j][1]*data[i][j][2]
                amount[i][3]-=data[i][j][2]
            else:   
                amount[i][2]+=amount[i][3]*data[i][j][1]
                amount[i][3]=0
            j-=1
        price[i]=round(((amount[i][2]/amount[i][1])/price[i]-1)*100,5)

    return price

def check_value():

    connection = sqlite3.connect('C:\git\Python-course-SI\cryptocurrency.db')
    cursor = connection.cursor()
    cursor.execute("SELECT Currency FROM wallet WHERE Amount>0")           
    currency=cursor.fetchall()
    print(currency)
    cursor.close()


    #currency=['BTC','ETH']
    amount=[1,1]
    value=[]
    for i in range(len(currency)):
        if amount[i]!=0:
            value.append(check(currency[i][0]))
    print(value)

def check(cur):
    switcher={
        'BTC':'https://www.bitstamp.net/api/v2/transactions/btcusd/',
        'BCH':'https://www.bitstamp.net/api/v2/transactions/bchusd/',
        'XRP':'https://www.bitstamp.net/api/v2/transactions/xrpusd/',
        'LTC':'https://www.bitstamp.net/api/v2/transactions/ltcusd/',
        'ETH':'https://www.bitstamp.net/api/v2/transactions/ethusd/'
    }
    url=switcher.get(cur)
    data={'time':'day'}
    single_value=requests.get(url, data= data).json()
    BTC,BTC_s=create_table(single_value,0)
    BTC=BTC[-1][1]-BTC[0][1]

    return BTC

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
    
def insert_data(mode):
    print("dodaje baze")
    connection = sqlite3.connect('C:\git\Python-course-SI\cryptocurrency.db')
    cursor = connection.cursor()
    command="""CREATE TABLE IF NOT EXISTS 
    wallet(Currency TEXT PRIMARY KEY, Amount REAL NOT NULL ) """
    cursor.execute(command)
    # pojawia się nowy paramet encoding ustawiony na utf-8
    with open('C:/git/Python-course-SI/btc.csv', 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',')
        for row in csvreader :
            if mode == 1:
                cur=(row['Currency'])
                cursor.execute("SELECT Amount FROM wallet WHERE Currency= ?", (cur,))
                value=cursor.fetchone()[0]
                value=value+float(row['Amount'])  
            else:
                value=  row['Amount']      
            data_tuple = (value,row['Currency'])
            cursor.execute("UPDATE wallet SET Amount=? WHERE Currency=?", data_tuple)           
            connection.commit()

    cursor.close()

def indirect(i):
    if i==1:
        money=int(input("Ile masz pieniedzy:"))
        program(money)
    if i=='2':
        insert_data(0)
    if i=='3':
        insert_data(1)
    if i=='4':
        check_value()
    if i=='5':
        print("End")
        sys.exit(0)

run=True
while run==True:
    print("1- Sprawdź zysk")
    print("2- Wprowadź nowe dane")
    print("3- Wprowadź zmiany w danych")
    print("4- Sprawdź wartość waluty")
    print("4- Koniec")
    x=input()
    indirect(x)
    

    print("Refresh")
