"""1. Rozszerzyć źródła danych o 2 kolejne API, 
porównywać wybrane wcześniej 2 pary zasobów i ich ceny kupna-sprzedaży na przestrzeni czasu. 
Tym razem na podstawie cen kupna / sprzedaży z pośród poszerzonej bazy macie za zadanie na bieżąco wyliczać czy występuje możliwość arbitrażu.
Pod pojęciem arbitrażu kryje się przeprowadzanie dwóch transakcji przeciwstawnych na dwóch różnych giełdach. 
Pisząc bardziej zrozumiale - sprawdzacie czy da się kupić taniej w miejscu 1 i sprzedać drożej w miejscu 2.
Pamiętajcie, że chcąc kupić w miejscu X musicie patrzeć na oferty sprzedaży w miejscu X, a chcąc sprzedać w miejscu Y musicie patrzeć na oferty kupna w miejscu Y.
Program, jak poprzedni, ma się automatycznie odświeżać. Wynikiem jego działania ma być print informacji(przykładowo):
Na giełdzie X można kupić 0.1 BTC za USD po kursie 6800 i sprzedać na giełdzie Y po kursie 6900, zyskując 10USD.
(5pkt)

2. Przy kalkulacjach wziąć pod uwagę prowizję kupna sprzedaży na giełdach. Pamiętajcie, żeby brać tu pod uwagę prowizję podawaną typu Taker (tę wyższą), bo bierzecie ofertę cudzą, nie składacie własnej i nie czekacie aż ktoś się na nią zdecyduje. 
(2.5pkt)

3. Założyć wirtualny budżet rozpatrywanych zasobów i w czasie rzeczywistym liczyć ile potencjalnie zarobilibyście na Waszych operacjach. Nie musicie brać pod uwagę opóźnienia w przesyłaniu środków pomiędzy giełdami.
Dla uproszczenia identyfikacji rozpatrywanego systemu zakładamy że dysponujemy środkami w każdej z rozpatrywanych walut na każdej z rozpatrywanych giełd. 
(2.5pkt)"""
import requests

def get_price():
    
    bitbay=requests.get('https://bitbay.net/API/Public/BTC/USD/ticker.json')
    cex=requests.get('https://cex.io/api/ticker/BTC/USD')
    bitstamp=requests.get('https://www.bitstamp.net/api/ticker')
    blockchain = requests.get("https://blockchain.info/ticker")
    return bitbay.json(),cex.json(),bitstamp.json(),blockchain.json()

def buy_sell():
    bitbay,cex,bitstamp,blockchain=get_price()

    

    bitbay_buy=bitbay['ask']
    bitbay_sell=bitbay['bid']

    cex_buy=cex['ask']
    cex_sell=cex['bid']

    bitstamp_buy=float(bitstamp['ask'])
    bitstamp_sell=float(bitstamp['bid'])

    blockchain_buy = blockchain["USD"]["buy"]
    blockchain_sell = blockchain["USD"]["sell"]

    name=['bitbay','cex','bitstamp','blockchain']
    taker=[1.03,1.03,1.025,1.024]
    buy=[bitbay_buy,cex_buy,bitstamp_buy,blockchain_buy]
    sell=[bitbay_sell,cex_sell,bitstamp_sell,blockchain_sell]
    for i in range(len(taker)):
        buy[i]=(taker[i]*buy[i]*0.2)
        sell[i]=(taker[i]*sell[i]*0.2)
        
    buy=max(zip(buy,name))
    same_index=name.index(buy[1])

    sell.pop(same_index)
    name.pop(same_index)
    sell=min(zip(sell,name))

    if buy[0]>sell[0]:
        print("sprzedaj 0,2 BTC w", buy[1],"za",buy[0], "kup w" ,sell[1],"za", sell[0],"zyskując", buy[0]-sell[0], "USD")
        wallet_file = open('C:/git/Python-course-SI/wallet.txt','r+')
        print (wallet_file.read())
        wallet = wallet_file.readlines()

    

        wallet_file.close()
    else:
        print("nie ma możliwości arbitrażu")
buy_sell()