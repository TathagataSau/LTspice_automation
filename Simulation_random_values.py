# -*- coding: utf-8 -*-
"""
Created on Sat May 20 14:30:32 2023

@author: Tathagata Sau
"""

import numpy as np 
#s= np.random.normal(4e-9 ,0.2e-9,200)
s= np.random.normal(0.3906012 ,0.01953006,200)
print(s)
s2=s.tolist()
x = [(-1 * value) for value in s2]
import csv 
with open('VTH_P_varition_Final.csv', 'w') as f:# Create a CSV writer object that will write to the file 'f'
    csv_writer = csv.writer(f)    # Write the field names (column headers) to the first row of the CSV file
    csv_writer.writerow(s2)
    reader = csv.reader('VTH_P_varition_Final.csv')
    data = list(reader)
    first_row = data[0]
    updated_row = [(value* -1) for value in first_row]
    data[0] = updated_row
    
import matplotlib.pyplot as plt
plt.figure()
plt.style.use('ggplot')
plt.hist(s2, bins=200)
plt.show()