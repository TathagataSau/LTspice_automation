# -*- coding: utf-8 -*-
"""
Created on Thu May 18 20:05:58 2023

@author: Tathagata Sau
"""

import numpy as np
import csv

# Parameters
Tox = 4.1E-9
num_values = 200
output_file = "D:\Acropolice\simulation_results.csv"
# Generate random values from normal distribution
values = np.random.normal(loc=0, scale=Tox, size=num_values)
# Calculate frequency values
frequency_values = np.histogram(values, bins=200)[0]  # Adjust the number of bins as desired

# Save data to CSV file
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Value", "Frequency"])  # Write header
    for value, frequency in zip(values, frequency_values):
        writer.writerow([value, frequency])
