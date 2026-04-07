import pandas as pd
import numpy as np

Fiber_df = pd.read_csv("Fiberbits.csv", header=0)
Fiber_df.head(3)
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

from sklearn.model_selection import GridSearchCV
tuned_parameters = [{'criterion': ['gini','entropy'],'max_depth': range(2,10)}]
#clf_tree = tree.DecisionTreeClassifier()
clf = GridSearchCV(clf1, tuned_parameters, cv=10, scoring='roc_auc')
clf.fit(X_train, y_train )

clf.best_score_

clf.best_params_

clf.grid_scores_