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

    data=bubbleSort(data,0)

    return data


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


def check_value(mode):

    connection = sqlite3.connect('C:\git\Python-course-SI\cryptocurrency.db')
    cursor = connection.cursor()
    cursor.execute("SELECT Currency FROM wallet WHERE Amount>0")           
    currency=cursor.fetchall()
    cursor.close()

    value=[]
    sum_now=0
    sum_past=0
    print("Tak zmieniła się wartość twoich walut:")
    for i in range(len(currency)):
        transactions=check(currency[i][0])
        if mode==0:
            value.append(transactions[-1][1]-transactions[0][1])
        else:
            value.append(round(transactions[-1][1]/transactions[0][1]-1,4))
        sum_now+=transactions[-1][1]
        sum_past+=transactions[0][1]
    for i in range(len(value)):
        if mode==0:
            print(currency[i][0],value[i])
        else: 
            print(currency[i][0],value[i],"%")
    if mode ==0:
        print("Sumarycznie twój portfel zmienił się o",sum_now-sum_past)
    else:
        print("Sumarycznie twój portfel zmienił się o",round(sum_now/sum_past-1,4),"%")

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
    BTC=create_table(single_value,0)
    return BTC


    
def insert_data(mode):
    connection = sqlite3.connect('C:\git\Python-course-SI\cryptocurrency.db')
    cursor = connection.cursor()
    cursor.execute("SELECT Currency FROM wallet")
    #currency_list=cursor.fetchall()
    select=cursor.fetchall()
    currency_list=[]
    for i in select:
        currency_list.append(i[0])
    print(currency_list)
 
    with open('C:/git/Python-course-SI/btc.csv', 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',')
        erors=[]
        for row in csvreader :
            if row['Currency'] in currency_list:
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
            else:
                erors.append(row['Currency'])
        if len(erors) >0:
            print("Próbowałeś dodać walutę której nie ma w systemie:", erors)

    cursor.close()

def print_data():
    connection = sqlite3.connect('C:\git\Python-course-SI\cryptocurrency.db')
    cursor = connection.cursor()
    cursor.execute("SELECT Currency,Amount FROM wallet WHERE Amount>0")           
    currency=cursor.fetchall()
    cursor.close()
    print("W bazie masz zapisane:")
    for i in currency:
        print("Waluta",i[0],"Ilość",i[1])

def indirect(i):
    if i=='1':
        check_value(1)
    if i=='2':
        check_value(0)   
    if i=='3':
        insert_data(0)
    if i=='4':
        print_data()
    if i=='5':
        insert_data(1)
    if i=='6':
        print("End")
        sys.exit(0)


while True:
    print("1- Sprawdź zysk procentowy")
    print("2- Sprawdź zysk liczbowy")
    print("3- Wprowadź dane do bazy")
    print("4- Wyświetl dane z bazy")
    print("5- Aktualizuj dane")
    print("6- Koniec")
    x=input("Wybierz opcję: ")
    indirect(x)
    

    print("Refresh")
