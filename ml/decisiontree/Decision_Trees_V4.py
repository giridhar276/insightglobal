#Import Data
import pandas as pd

##Ecom_Cust_Survey = pd.read_csv('...',header = 0)
df = pd.read_csv('Ecom_Cust_Survey.csv',header = 0)

df.dropna(inplace=True) # to remove all the missing values rows..
#Q 1. How many customers have participated in the survey?
df.info()
#ANS: 11805

#Q.2 Overall most of the customers are satisfied or dis-satisfied?
#total number of customers
df.shape

#number of satisfied customers
freq=df['Overall_Satisfaction'].value_counts(sort=False)
print(freq)


#Q 3. Can you segment the data and find the concentrated satisfied and dis-satisfied customer segments ?
#solution:
# We will create a tree model in python using the sci-kit module
# before that we will need to convert most of the feature data into numerical or hash values as scikit only works with numerical data


df['Region'] = df['Region'].map( {'EAST': 1, 'WEST': 2, 'NORTH': 3, 'SOUTH':4} ).astype(int)
df['Customer_Type'] = df['Customer_Type'].map({'Prime': 1, 'Non_Prime': 0}).astype(int)

#We will also need to change the column names, as '.' and spaces are part of many basic function in python
df.rename(columns={'Order Quantity':'Order_Quantity', 'Improvement Area' :'Improvement_Area'}, inplace=True)
df['Improvement_Area'] = df['Improvement_Area'].map({'Website UI':1, 'Packing & Shipping':2, 'Product Quality':3,}).astype(int)
df['Overall_Satisfaction'] = df['Overall_Satisfaction'].map( {'Dis Satisfied': 0, 'Satisfied': 1} ).astype(int)

#Need the library to create the tree
from sklearn import tree

#Defining Features and lables, ignoring cust_num and target variable
features= list(df.columns[2:6])

X = df[features]
y = df['Overall_Satisfaction']

#Building Tree Model
clf = tree.DecisionTreeClassifier(max_depth=2)
clf.fit(X,y)

#What are the major characteristics of satisfied customers?

#Plotting the trees
#Unfortunately drawing a beautiful tree is not easy in python, Still
#you will need to install pydot
#use this command in your anaconda prompt: conda install -c anaconda pydot=1.0.28

from IPython.display import Image
from sklearn.externals.six import StringIO

#First run below command on Anaconda Conslole and Install pydotplus manulaly otherwise import pydotplus throws an error
#pip install pydotplus 

#Before drawing the graph below command on anaconda console
#pip install graphviz

import pydotplus

dot_data = StringIO()
tree.export_graphviz(clf,
                     out_file = dot_data,
                     feature_names = features,
                     filled=True, rounded=True,
                     impurity=False)

graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())


#by looking at the plot we can answer two questions:
#Q.5 What are the major characteristics of satisfied customers?

#Major_characteristics= Order.Quantity<40 & Age<30 | Order.Quantity >=40

#Q 6. What are the major characteristics of dis-satisfied customers?
#Major_characteristics= Order.Quantity<40 & Age>=30

#LAB : Tree Validation
########################################
##########Tree Validation
#Tree Validation
X
predict1 = clf.predict(X)
predict1


from sklearn.metrics import confusion_matrix ###for using confusion matrix###
cm = confusion_matrix(y, predict1)
print (cm)

total = sum(sum(cm))
#####from confusion matrix calculate accuracy
accuracy = (cm[0,0]+cm[1,1])/total
print(accuracy)


#LAB: Overfitting
#LAB: The problem of overfitting
############################################################################ 
##The problem of overfitting
#Choosing Cp and Pruning


#Dataset: "Buyers Profiles/Train_data.csv"
#Task 1: Import both test and training data
import pandas as pd
#Dataset: "Buyers Profiles/Train_data.csv"
#Import both test and training data
train = pd.read_csv("Train_data.csv", header=0)
test = pd.read_csv("Test_data.csv", header=0)

##print train.info()
train.shape
test.shape

# Building the tree model.
# the data have string values we need to convert them into numerica values
train['Gender'] = train['Gender'].map( {'Male': 1, 'Female': 0} ).astype(int)
train['Bought'] = train['Bought'].map({'Yes':1, 'No':0}).astype(int)

test['Gender'] = test['Gender'].map( {'Male': 1, 'Female': 0} ).astype(int)
test['Bought'] = test['Bought'].map({'Yes':1, 'No':0}).astype(int)

##print train.info()
##print test.info()

from sklearn import tree

#Defining Features and lables
features = list(train.columns[:2])

X_train = train[features]
y_train = train['Bought']

#X_train

X_test = test[features]
y_test = test['Bought']

#training Tree Model
clf = tree.DecisionTreeClassifier()
clf.fit(X_train,y_train)

#Plotting the trees
#Unfortunately drawing a beautiful tree is not easy in python, Still
#you will need to install pydot
#use this command in your anaconda prompt: conda install -c anaconda pydot=1.0.28
from IPython.display import Image
from sklearn.externals.six import StringIO
import pydotplus
dot_data = StringIO()
tree.export_graphviz(clf,
                     out_file = dot_data,
                     feature_names = features,
                     filled=True, rounded=True,
                     impurity=False)

graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())

predict1 = clf.predict(X_train)
print(predict1)

predict2 = clf.predict(X_test)
print(predict2)

####Calculation of Accuracy and Confusion Matrix
#on the train data
from sklearn.metrics import confusion_matrix ###for using confusion matrix###
cm1 = confusion_matrix(y_train,predict1)
cm1
total1 = sum(sum(cm1))
#####from confusion matrix calculate accuracy
accuracy1 = (cm1[0,0]+cm1[1,1])/total1
accuracy1


#On Test Data
cm2 = confusion_matrix(y_test,predict2)
cm2
total2 = sum(sum(cm2))
#####from confusion matrix calculate accuracy
accuracy2 = (cm2[0,0]+cm2[1,1])/total2
accuracy2

#LAB: Pruning

### hyper parameters : Before creating the model ,we pass some values 
### model parameters : after creating the model

#We will rebuild a new tree by using above data and see how it works by tweeking the parameteres we have..
dtree = tree.DecisionTreeClassifier(max_leaf_nodes = 10, 
                                    min_samples_leaf = 5, 
                                    max_depth= 5)
dtree.fit(X_train,y_train)

predict3 = dtree.predict(X_train)
predict4 = dtree.predict(X_test)

#Accuracy of the model that we created with modified model parameters.
#on the train data
from sklearn.metrics import confusion_matrix ###for using confusion matrix###
cm1 = confusion_matrix(y_train,predict3)
cm1
total1 = sum(sum(cm1))
#####from confusion matrix calculate accuracy
accuracy1 = (cm1[0,0]+cm1[1,1])/total1
accuracy1


#On Test Data
cm2 = confusion_matrix(y_test,predict4)
cm2
total2 = sum(sum(cm2))
#####from confusion matrix calculate accuracy
accuracy2 = (cm2[0,0]+cm2[1,1])/total2
accuracy2

#the new model Dtree is giving us an accuracy of 83%(Not Bad Huh)
#We can work on more of the parameers that are mentioned in the decision tree documentation on:
#http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier


#LAB: Tree Building & Model Selection
#We will try to build a few trees tweeking the parameteres of the tree and see which works best
#Dataset: Fiber bits

import pandas as pd
import numpy as np

Fiber_df = pd.read_csv("Fiberbits.csv", header=0)

Fiber_df.info()

#good thing the data have all the values as numerical
#Modeling a decision tree
from sklearn import cross_validation, tree

#Defining Features and lables
features = list(Fiber_df.drop(['active_cust'],1).columns) #this code gives a list of column names except 'active_cust'

X = np.array(Fiber_df[features])
y = np.array(Fiber_df['active_cust'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y, train_size = 0.8)

#Tree building and validation

clf1 = tree.DecisionTreeClassifier()
clf1.fit(X_train,y_train)


#If we want to see the predictive values we can do this by:
#predict1 = clf1.predict(y_train)
clf1.score(X_train,y_train)

clf1.score(X_test,y_test)
#This model with default parameters is giving us accuracy of 99% on training and 84.505..% 
#It is overfitted model with defalut parameters

#Let's make a model by chnaging the parameters.
clf2 = tree.DecisionTreeClassifier(criterion='gini', 
                                   splitter='best', 
                                   max_depth=20, 
                                   min_samples_split=5, 
                                   min_samples_leaf=5, 
                                   max_leaf_nodes=10)
clf2.fit(X_train,y_train)
clf2.score(X_train,y_train)

clf2.score(X_test,y_test)
#we were able to get our score up to 85.1585%



#Finding optimal criteria and max_depth
# optimal hyper parameters
from sklearn.model_selection import GridSearchCV
tuned_parameters = [{'criterion': ['gini','entropy'],'max_depth': range(2,10)}]
clf_tree = tree.DecisionTreeClassifier()
clf = GridSearchCV(clf1, tuned_parameters, cv=10, scoring='roc_auc')
clf.fit(X_train, y_train )

clf.best_score_

clf.best_params_

clf.grid_scores_
