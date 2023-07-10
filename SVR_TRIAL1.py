# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 13:15:43 2023

@author: Tathagata Sau
"""

import pandas as pd
from sklearn.svm import SVR
from sklearn.impute import SimpleImputer
data = pd.read_csv('your_file.csv')
X = data.drop(columns=['target_column'])
y = data['target_column']
imputer = SimpleImputer()
X_imputed = imputer.fit_transform(X)
model = SVR(kernel='linear')
model.fit(X_imputed, y)
X_missing = data[data.isnull().any(axis=1)].drop(columns=['target_column'])
y_predicted = model.predict(X_missing)
data.loc[data['target_column'].isnull(), 'target_column'] = y_predicted
