# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 21:07:12 2023

@author: Tathagata Sau
"""

dir_XVIIx64 = "C:\Program Files\LTC\LTspiceXVII"

import subprocess

#%%
Txt_original = 'Project_2nd_LPF_TRAN.txt'
Res1_original = 'Res1 = 1k'
Cap1_original = 'Cap = 0.1u'  #original variaable values

with open(Txt_original,'rb') as file:
    Data_original = file.read()
#    print(Data_original)
    Data_temp = Data_original.replace(Res1_original.encode('ascii'), 'Res1 = 10k' .encode('ascii'))\
    .replace(Cap1_original.encode('ascii'), 'Cap1 = 1u' .encode('ascii'))
with open('new_python.txt', 'wb') as file:
    file.write(Data_temp)
    #%%
subprocess.call(dir_XVIIx64 + "\XVIIx64.exe -b new_Python.txt")