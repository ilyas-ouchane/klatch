import numpy as np
import matplotlib.pyplot as plt

import sklearn
from sklearn import datasets
from sklearn import svm 
from sklearn import metrics

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

# pd.set_option('display.width', 5000
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import sklearn
from sklearn import svm
from sklearn import metrics
import pandas as pd
import numpy as np
from sklearn import linear_model


from sklearn import svm
from sklearn import metrics
import pickle
import pandas as pd
import numpy as np

import pickle
import random
import time


data = pd.read_csv('5clustKlatch.csv', sep=';')
data = data[['Music', 'Hiphop, Rap', 'Raggae', 'Swing, Jazz', 'Movies',
       'Comedy', 'Romantic', 'Sci-fi', 'War', 'Fantasy/Fairy tales',
       'Documentary', 'Western', 'History', 'Psychology', 'Politics',
       'Reading', 'Languages', 'Musical instruments', 'Writing', 'Sport',
       'Celebrities', 'Science and technology', 'Theatre', 'Age', 'Gender',
       'clusters']]
predict = 'clusters'

X = np.array(data.drop([predict], 1))
Y = np.array(data[predict])

X=X.astype('int')
Y=Y.astype('int')


x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.1)


clf = svm.SVC(kernel="linear") #On peut donner en paramètre kernel and soft margin of the hyperplan
clf.fit(x_train, y_train)


# clf.fit(x_train, y_train)

y_pred = clf.predict(x_test) # Predict values for our test data

acc = metrics.accuracy_score(y_test, y_pred) # Test them against our correct values

scores = cross_val_score(clf, X, Y, cv=30)

# print("Accuracy:%0.2f(+/- %0.2f at best)" % (scores.mean(), scores.std() * 2))

# print("Scores for 30 : ",scores)


# def test_model(list_user):
#     import pickle
#     import numpy as np
# #     pickle.dump(clf, open(fn, 'wb'))
#     filename = 'final_model_klatch.sav'
#     loaded_model = pickle.load(open(filename, 'rb'))
#     A = np.array([list_user])
#     B = A.reshape(1,-1)
#     result = loaded_model.predict(B)
#     return(result[0])

# test_model([4,2,2,4,2,5,2,1,5,2,2,3,5,4,5,4,2,3,4,3,4,5,3,22,0])
pickle.dump(clf, open('final_model_klatch.sav', 'wb'))
loaded_model = pickle.load(open('final_model_klatch.sav', 'rb'))
A = np.array([4,2,2,4,2,5,2,1,5,2,2,3,5,4,5,4,2,3,4,3,4,5,3,22,0])
B = A.reshape(1,-1)
result = loaded_model.predict(B)
print(result)