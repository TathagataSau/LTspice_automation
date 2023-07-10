# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 20:31:07 2023

@author: Tathagata Sau
"""

dir_XVIIx64 = "C:\Program Files\LTC\LTspiceXVII"

import subprocess


subprocess.call(dir_XVIIx64 +"\XVIIx64 -Run Project_2nd_LPF_TRAN.asc")
#%%
subprocess.call(dir_XVIIx64 +"\XVIIx64 -b Project_2nd_LPF_TRAN.asc")
#%%
subprocess.call(dir_XVIIx64 +"\XVIIx64 -Run Project_2nd_LPF_TRAN.cir")
#%%
subprocess.call(dir_XVIIx64 +"\XVIIx64 -b Project_2nd_LPF_TRAN.cir")