import random
import requests
from matplotlib.pyplot import *
def get_data():
    data=[1,2,3,4,0,6,7,8,0]
    return data
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
   # plot(data+new_data)
    #show()
#old_data=[1,3,5,6,3,2,6,7,8,9]
time=[0,1,2,3,4,5,6,7,8]
time2=[8,9,10,11,12,13,14,15,16,17]
old_data=get_data()
average=[0]*(len(old_data)+1)
for i in range(100):
    new_data=analyse_data(old_data)
    for i in range(len(new_data)):
        average[i]+=new_data[i]
    print(new_data)
    print(average,"avg")
for i in range(len(average)):
    average[i]=average[i]/100   
print(average)
plot(time,old_data,'b')
plot(time2,average,'r')
plot(time2,new_data,'g')
show()    
