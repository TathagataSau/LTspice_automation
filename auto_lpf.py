# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 18:49:22 2023

@author: Tathagata Sau
"""


#%% for loop to make the names of all combinations of simulation cases

origR1 = 'Res1 = 1k'
origC1 = 'cap1 = 0.1u'
oeigR2 = 'Res2 = 1k'
origC2 = 'Cap2 = 0.1u'

listR1 = ['Res1 = 1k','Res1=10k']
listC1 = ['Cap1 = 0.1u','Cap1=1u']
listR2 = ['Res2 = 1k','Res2=10k']
listC2 = ['Cap2 = 0.1u','Cap2=1u']
listALL =[]
for x in range(len(listR1)):
    for y in range(len(listC1)):
        for z in range(len(listR2)):
            for a in range(len(listC2)):
                listALL.append(listR1[x] +'_'+ listC1[y] + '_' +listR2[z]+ '_' + listC2[a])
                
#%% create the subdirectory
import os
cwd = os.getcwd() #current working dictionary of ltspice .asc file
#crteate a subfolder to save the variation of Ltspice simulation files

try:
    os.mkdir('SimFolder') #no whitespaces
except:
    print("THE FOLDER ALREADY EXISTS!")
    
    orig = "Project_2nd_LPF_TRAN" #without extention
    origTxt = orig + '.txt' #To run .cir file name must have no whitespaces
    
#%%
import time
start = time.time()
print("begin...")



dir_XVIIx64 = "C:\Program Files\LTC\LTspiceXVII"

import subprocess

iter = 0 #iteration
listALL = [] #All txt files names, dimension = Len(x)*Len(Y)*...e.g., = 3^4 = 81
for r1 in listR1:
    for c1 in listC1:
        for r2 in listR2:
            for c2 in listC2:
                newFileName = r1 + '_' + c1 + '_' + r2 + '_'+ c2
                newFileTxt = newFileName + '.txt'
                listALL.append(newFileName) #save each file name into listALL
                with open(origTxt, 'rb') as file:#real in the file
                    origData = file.read()
                    tempData = origData.replace(origR1.encode('ascii'),r1.encode('ascii'))\
                        .replace(origC1.encode('ascii'), c1.encode('ascii'))\
                        .replace(origR1.encode('ascii'), r2.encode('ascii'))\
                        .replace(origC2.encode('ascii'), c2.encode('ascii'))
                with open('SimFolder/' + newFileTxt, 'wb') as file:
                    file.write(tempData)
                iter += 1 #print out thr current itteration
                print('to run txt file #:',iter,'over total 16 has as file name:', newFileName)
                #run LTspice in  the for loop
                subprocess .call(dir_XVIIx64+'/XVIIx64 -b ' + 'simFolder/'+ newFileTxt)
                
end = time.time()
print("done")
print("~~~~~~~~~~~~~Time elapsed is", end - start,"~~~~~~~~~~~")
                

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#%% Read new data



import ltspy3
import matplotlib.pyplot as plt



try:
    os.mkdir('FigFolder')# no whitespace
except:
    print('The Folder already Exists!')
    
    
import time
start = time.time()
print("begin...")


# ************************ Read data into python IDE **********************
iter = 0 #iteration
for eachFile in listALL:
    if '' in eachFile:
        print(eachFile)
        sd = ltspy3.SimData('SimFolder/'+ eachFile+ '.raw')#.raw in a string
        name = sd.variables #variables from teh raw data
        time_trace = sd.values #time and traces from the raw data
        time_Axis = sd.values[0] #first element of the time in t6he matrix
        trace_Axis = sd.values[1:3] # rest elements are traced in the matrix
#plot
#   %matplot qt
#if you want the graphs saved in, save as figure
#
#  %matplotlib
#want an inline plot

        plt.figure(1)
        plt.plot(time_Axis,trace_Axis[0], 'r-', linewidth = 2, label = 'the 1st variable V(in)')
        plt.plot(time_Axis,trace_Axis[1], 'b-', linewidth = 2, label = 'the 2nd variable V(out)')
        plt.legend(loc = 'upper right', shadow = True, fontsize = '10')
        plt.xabel("Time(sec)", fontsize = 12, color = 'black')
        plt.ylabel('voltage(V)', fontsize = 12, color = 'black')
        plt.xlim()
        plt.ylim()
        plt.grid(True)
        plt.suptitle(eachFile, fontsize = 14, color  = 'black')
        plt.show()
#save as a seperate figure
        plt.savefig("FigFolder/" + eachFile + '.png',dpi = 150)
        plt.close("all") #close all figures
        iter += 1 #print out the current itteration
        print('To plot figure #:',iter,'over total 16 has a file name', newFileName)
        
        
end = time.time()
print("done!")
print("~~~~~~~~~~~~~~ Time elapsed is:", end - start,"~~~~~~~~~~~~~")