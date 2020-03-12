import numpy as np

def bubbleSort(data):
    lenght=len(data)
    swapped= True    
    while (swapped == True):
        swapped= False
        for i in range(lenght-1):
            if data[i]>data[i+1]:
                data[i], data[i+1] = data[i+1], data[i] 
                swapped = True

    return data
   
def insertionSort(data): 

    for i in range(1, len(data)): 
        key = data[i] 
        j = i-1
        while j >= 0 and key < data[j] : 
                data[j + 1] = data[j] 
                j -= 1
        data[j + 1] = key

    return data

print("bubbleSort")
data=np.random.randint(-10,20,10)
print(data)
print(bubbleSort(data))
print("insertionSort")
data=np.random.randint(-10,20,10)
print(data)
print(insertionSort(data))
