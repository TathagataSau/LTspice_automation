# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 20:46:11 2023

@author: Tathagata Sau
"""

dir_XVIIx64 = "C:\Program Files\LTC\LTspiceXVII"

import subprocess

subprocess.call(dir_XVIIx64 + "\XVIIx64.exe -b Project_2nd_LPF_TRAN.cir")