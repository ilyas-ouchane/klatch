from sklearn import svm
from sklearn import metrics
import pickle
import pandas as pd
import numpy as np

A = np.array() #We give the list of the attributes of the database including gender and age 
B = A.reshape(1, -1)
filename = 'C:/Users/abirabir/Desktop/Data/finalized_model2.sav' #path to .sav file 
loaded_model = pickle.load(open(filename, 'rb')) 
result = loaded_model.predict(B)
print(result) #This should print the cluster predicted
