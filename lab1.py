import numpy as np
import time

def bubbleSort(data,index):
    lenght=len(data)
    swapped= True    
    while (swapped == True):
        swapped= False
        for i in range(lenght-1):
            if data[i]<data[i+1]:
                index[i], index[i+1] = index[i+1], index[i]
                data[i], data[i+1] = data[i+1], data[i] 
                swapped = True

    return index
   
def insertionSort(data,index): 

    for i in range(1, len(data)): 
        key = data[i] 
        key2= index[i]
        j = i-1
        while j >= 0 and key > data[j] : 
                index[j+1]=index[j]
                data[j + 1] = data[j] 
                j -= 1
        data[j + 1] = key
        index[j+1]= key2
    return index

def bubbleSort_onSets(set,param):
    start = time.clock()
    numbers=0
    i=0
    result=[]
    index=[]
    while(numbers<3  and i< len(set)):
        if(set[i]>param):
            result.append(set[i])
            index.append(i)
            numbers=numbers+1
        i=i+1  
    duration = time.clock() - start
    return bubbleSort(result,index),duration

def insertionSort_onSets(set,param):
    start=time.clock()
    numbers=0
    i=0
    result=[]
    index=[]
    while(numbers<3 and i<len(set)):
        if(set[i]>param):
            result.append(set[i])
            index.append(i)
            numbers=numbers+1
        i=i+1  
        duration=time.clock()-start
    return insertionSort(result,index) ,duration


print("BubbleSort")
data=np.random.randint(-10,20,10)
print(data)
tab,time1=bubbleSort_onSets(data,10)
print(tab)
print("InsertionSort")
data=np.random.randint(-10,20,10)
print(data)
tab,time2=insertionSort_onSets(data,10)
print(tab)
print("time of BubbleSort - time of InsertionSort")
print(time1-time2)
