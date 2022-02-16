"""
Created on Mon Nov 22 13:40:14 2021

@author: alex
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#importing boston housing data
from sklearn.datasets import load_boston
boston_dataset = load_boston() 

#creating a dataframe for easier data manipulation later
boston = pd.DataFrame(boston_dataset.data, 
                      columns=boston_dataset.feature_names)
boston['MEDV'] = boston_dataset.target #adding target to df

#inspecting data
print(boston.shape)
print(boston.columns)
print(boston[['CHAS', 'RM', 'AGE', 'RAD', 'MEDV']].head()) #checking dtypes
print(boston.describe().round(2)) #summary stats

#visualizing data column by column
boston.hist(column='RM', bins=20)
plt.savefig("plot1.png")
plt.show()

#checking which measures have high correlation
corr_matrix = boston.corr().round(2) #creates correlation matrix
boston.plot(kind = 'scatter',
  x = 'RM',
  y = 'MEDV',
  figsize=(8,6))
plt.savefig("plot1.png") #visualizes relationship w/ target
plt.show()
boston.plot(kind = 'scatter',
  x = 'LSTAT',
  y = 'MEDV',
  figsize=(8,6))
plt.savefig("plot1.png") #visualizes relationship w/ target
plt.show()

#defining model variables
X = boston[['RM']]
Y = boston['MEDV']

"""FITTING THE MODEL"""
from sklearn.linear_model import LinearRegression #imports linreg class
model = LinearRegression() #creates instance of the class
#splitting data into testing and training sets
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state=1)

model.fit(X_train, Y_train)
print(model.intercept_.round(2)) #shows model intercept
print(model.coef_.round(2)) #shows model slope

"""PREDICTION"""
new_RM = np.array([6.5]).reshape(-1,1) # make sure it's 2d
print(model.predict(new_RM))
#feeding entire testing set
y_test_predicted = model.predict(X_test)
print(y_test_predicted.shape)
print(type(y_test_predicted))

"""EVALUATION"""
#show data and model on same graph
plt.scatter(X_test, Y_test,
label='testing data');
plt.plot(X_test, y_test_predicted,
label='prediction', linewidth=3)
plt.xlabel('RM'); plt.ylabel('MEDV')
plt.legend(loc='upper left')
plt.savefig("plot.png")
plt.show()

##Residuals
residuals = Y_test - y_test_predicted #calculating residuals
plt.scatter(X_test, residuals) #plot the residuals
#plot a horizontal line at y = 0
plt.hlines(y = 0,
xmin = X_test.min(), xmax=X_test.max(),
linestyle='--')
#set xlim
plt.xlim((4, 9))
plt.xlabel('RM'); plt.ylabel('residuals')
plt.savefig("plot.png")
plt.show()

#Mean Squared Error
from sklearn.metrics import mean_squared_error
print(mean_squared_error(Y_test, y_test_predicted))
#or
print((residuals**2).mean())

#R-squared
from sklearn.metrics import mean_squared_error
print(model.score(X_test, Y_test))

"""Multivariate Linear Regression"""

## data preparation
X2 = boston[['RM', 'LSTAT']]
Y = boston['MEDV']
## train test split
## same random_state to ensure the same splits
X2_train, X2_test, Y_train, Y_test = train_test_split(X2, Y, 
                                                    test_size = 0.3, 
                                                    random_state=1)
model2 = LinearRegression()
model2.fit(X2_train, Y_train)
print(model2.intercept_)
print(model2.coef_)
#applying model
y_test_predicted2 = model2.predict(X2_test)
print(y_test_predicted2)

"""COMPARING MODELS"""
print(mean_squared_error(Y_test, y_test_predicted).round(2))
print(mean_squared_error(Y_test, y_test_predicted2).round(2))










