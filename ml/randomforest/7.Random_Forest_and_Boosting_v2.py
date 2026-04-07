import pandas as pd
import sklearn as sk
import numpy as np
import scipy as sp

#Importing dataset
car_train=pd.read_csv(".\\Datasets\\Car Accidents IOT\\train.csv")
car_test=pd.read_csv(".\\Datasets\\Car Accidents IOT\\test.csv")

from sklearn import tree

var=list(car_train.columns[1:22])
c=car_train[var]
d=car_train['Fatal']

###buildng Decision tree on the training data ####
clf = tree.DecisionTreeClassifier()
clf.fit(c,d)

#####predicting on test data ####
tree_predict=clf.predict(car_test[var])

from sklearn.metrics import confusion_matrix###for using confusion matrix###
cm1 = confusion_matrix(car_test[['Fatal']],tree_predict)
print(cm1)

#####from confusion matrix calculate accuracy
total1=sum(sum(cm1))
accuracy_tree=(cm1[0,0]+cm1[1,1])/total1
accuracy_tree


####Building Random Forest Model
from sklearn.ensemble import RandomForestClassifier
forest=RandomForestClassifier(n_estimators=10,  max_features = 5)



forest.fit(c,d)

forestpredict_test=forest.predict(car_test[var])
e=car_test['Fatal']
e

###check the accuracy on test data
from sklearn.metrics import confusion_matrix###for using confusion matrix###
cm2 = confusion_matrix(car_test[['Fatal']],forestpredict_test)
print(cm2)
total2=sum(sum(cm2))
#####from confusion matrix calculate accuracy
accuracy_forest=(cm2[0,0]+cm2[1,1])/total2
accuracy_forest

##################################################################
#################LAB: Boosting

#importing the datasets
menu_train=pd.read_csv(".\\Datasets\\Ecom_Products_Menu\\train.csv")
menu_test=pd.read_csv(".\\Datasets\\Ecom_Products_Menu\\test.csv")

lab=list(menu_train.columns[1:101])
g=menu_train[lab]
h=menu_train['Category']

menu_train['Category'].value_counts()

###buildng Decision tree on the training data ####
from sklearn import tree
tree = tree.DecisionTreeClassifier()
tree.fit(g,h)

#####predicting on test data ####
tree_predict=tree.predict(menu_test[lab])

from sklearn.metrics import confusion_matrix###for using confusion matrix###
cm1 = confusion_matrix(menu_test['Category'],tree_predict)
print(cm1)

#####from confusion matrix calculate accuracy


#####predicting the tree  on test data ####
tree_predict=tree.predict(menu_test[lab])
from sklearn.metrics import f1_score
f1_score(menu_test['Category'], tree_predict, average='micro')


##Gradient BOOSTING ##

###Building a gradient boosting clssifier ###
from sklearn import ensemble
from sklearn.ensemble import GradientBoostingClassifier
boost=GradientBoostingClassifier(loss='deviance', 
                                 learning_rate=0.1, 
                                 n_estimators=100, #Number of iterations
                                 min_samples_leaf=5,  
                                 max_depth=3,  
                                 verbose=1) 

##calculating the time while fitting the Gradient boosting classifier
import datetime
start_time = datetime.datetime.now()
##fitting the gradient boost classifier
boost.fit(g,h)
end_time = datetime.datetime.now()
print(end_time-start_time)



###predicting Gradient boosting model on the test Data
boost_predict=boost.predict(menu_test[lab])
from sklearn.metrics import confusion_matrix###for using confusion matrix###
cm2 = confusion_matrix(menu_test['Category'],boost_predict)
print(cm2)


from sklearn.metrics import f1_score
f1_score(menu_test['Category'], boost_predict, average='micro') 







