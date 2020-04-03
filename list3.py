###1. Znaleźć w internecie API ze źródłem danych o rynkach finansowych, przykłady:
#https://bittrex.github.io/api/v1-1
#https://bitbay.net/en/public-api
#https://www.tradingview.com/rest-api-spec/#section/Authentication

#Stworzyć prostą funkcję, która łączy się z danym API, 
# pobiera listę ofert kupna oraz listę ofert sprzedaży i printuje do konsoli. (5pkt)

#2. Znaleźć API z drugiego źródła - giełdy / instytucji finansowej, 
# wybrać jeden zasób finansowy, a właściwie ich parę (bitcoin-usd / ropa-usd / złoto-usd / eur - usd) 
#porównać gdzie bardziej opłaca się kupić (oferty sprzedaży są niższe), 
# a gdzie sprzedać (oferty kupna są wyższe) (5pkt)
#GET https://cex.io/api/order_book/BTC/LTC/
#https://bitbay.net/API/Public/BTC/LTC/orderbook.json
import requests

def bitbay():
    
    data=requests.get('https://bitbay.net/API/Public/BTC/USD/orderbook.json')
    return data.json()

def bitbay_ticker():
    
    data=requests.get('https://bitbay.net/API/Public/BTC/USD/ticker.json')
    return data.json()    
def cex():
    
    data=requests.get('https://cex.io/api/ticker/BTC/USD')
    return data.json()

def buy_sell():
    data=bitbay()
    buy=data['bids'][:5]
    print("buy")
    for i in buy :
        print(i)
    print("sell")
    sell=data['asks'][:5]
    for i in sell :
        print(i)


buy_sell()

cex_ticker = cex()
bitbay_tickers = bitbay_ticker()

ASK_bitbay = bitbay_tickers['ask']
BID_bitbay = bitbay_tickers['bid']

ASK_cex = cex_ticker['ask']
BID_cex = cex_ticker['bid']

if ASK_bitbay > ASK_cex:
    print("Better buy in Cex")
else: 
    print("Better buy in Bitbay")
if BID_bitbay > BID_cex:
    print("Better sell in Bitbay")
else:
     print("Better sell in Cex")