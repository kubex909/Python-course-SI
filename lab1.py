import numpy as np

def bubblesort(data):
    lenght=len(data)
    swapped= True
    while (swapped == True):
        swapped= False
        for i in range(lenght-1):
            if data[i]>data[i+1]:
                data[i], data[i+1] = data[i+1], data[i] 
                swapped = True
    return data
  
#def quicksort(data):



data=np.random.randint(-10,20,10)
print(data)
print(bubblesort(data))