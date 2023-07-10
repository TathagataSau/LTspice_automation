# -*- Tox_Vth_variation -*-
"""
Created on Sun Jun  4 19:01:36 2023

@author: Tathagata Sau
"""

import systemcode as m
import os
import matplotlib.pyplot as plt
import xlsxwriter
import numpy as np
import pandas as pd
import os
import subprocess
import ltspy3
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn import metrics
from scipy.stats import skew
from scipy.stats import kurtosis

def chplot(n1,n2):

    ltspice_exe_path = r'C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe' #### can't find
    netlist_path = r"E:\PROECT_Main\LTspiceXVII\LTspiceXVII\tmp5.cir" #done
    subprocess.call([ltspice_exe_path, '-Run', netlist_path])
    path = r'E:\PROECT_Main\LTspiceXVII\LTspiceXVII'
    filename = "tmp5"
    path += '\\tmp5.raw'
    sd = ltspy3.SimData(filename=path)  
    name = sd.variables  
    freq_complex = sd.values  
    a = sd.values[n1]  
    b = sd.values[n2]  
    for i in range(201):
        plt.plot(a[0], b[i]*(-1))
    plt.xlabel('VDD(v)')
    plt.ylabel('I_out(nA)')
    plt.title('powersupplysensitivity for ch')
    v = len(a[0])  
    for j in range(v):
        if round(a[0][j], 2) >= 1.30:
            x = j
            break
    l1 = []
    for i in range(201):
        l1.append(b[i][x]*(-1))  
    l2 = []
    for i in range(int(170e-9 / 0.1e-9), int(190e-9 / 0.1e-9)):
        wavelength = (i * 0.1e-9)
        l2.append(wavelength)
    plt.show()
    createexcel(l1,l2)
    return l1

def createexcel(l1, l2):

    user_input = input("Please give a name for the channel length excel file : ") 
    newDataframe = pd.DataFrame()
    newDataframe['Channel Length'] = l2[0:201]
    newDataframe['I(A)'] = l1[0:201]
    newDataframe.to_excel(user_input+".xlsx", index = False)

def custom_SVM(df1):

    df=df1
    X = df.iloc[:, 1].values
    y = df.iloc[:, 0].values

    from sklearn.preprocessing import StandardScaler
    sc_X=StandardScaler()  
    sc_y=StandardScaler()
    X=sc_X.fit_transform(X.reshape(-1,1))
    y=sc_y.fit_transform(y.reshape(-1,1))

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test =  train_test_split(X,y,test_size=0.2)

    from sklearn.svm import SVR
    regressor=SVR(C=0.1, gamma=0.01, kernel='rbf')
    regressor.fit(X_train.reshape(-1,1), y_train.reshape(-1,1))
    y_pred = regressor.predict(X_test.reshape(-1,1))
    y_pred = sc_y.inverse_transform(y_pred.reshape(-1,1))
    y_pred=y_pred.ravel()
    z = sc_y.inverse_transform(y_test)
    print(z.ravel())
    c = df['I_out(nA)']
    res = []
    for mem in z.ravel():
        for i, mem1 in enumerate(c):
            if mem == mem1:
                res.append(df['tox values'][i])
    df = pd.DataFrame({'Tox': res, 'Real Values': z.ravel()[0:len(res)], 'Predicted Values': y_pred[0:len(res)]})
    print(df.to_string())

    mean=sum(y_pred)/len(y_pred)
    s=skew(y_pred)
    k=kurtosis(y_pred)
    print("For Predicted Values : ")
    print("Mean value is: ",mean)
    print("kurtosis value is: ",k)
    print("skewness value is: ",s)

    print('Mean Absolute Error is : ')
    print(metrics.mean_absolute_error(y_test,y_pred))
    print('Mean Squared Error is : ')
    print(metrics.mean_squared_error(y_test,y_pred))
    print('Root Mean Squared Error is :')
    print(np.sqrt(metrics.mean_squared_error(y_test,y_pred)))

def plot(current,n,n1):

    plot2=plt.figure(2)
    plt.hist(current,bins=n1)
    plt.xlabel('I_out(nA)')
    plt.ylabel('Frequency')
    if n==1:
        plt.title('I_out(nA) for tox values')
    elif(n==2):
        plt.title('I_out(nA) for vth values')
    else:
        plt.title('I_out(nA) for both variation')
    plt.show() 

def pathmodification(txtfile):

    l=txtfile.split('\\')
    l.pop(len(l)-1)
    path='\\'.join(l)
    return path 
  
def toxxl(current,tox,filename,path,n):

    path1 = "E:\PROECT_Main\LTspiceXVII\LTspiceXVII" 
    dir_list = os.listdir(path1)
    if('tox_n_varition_Final.xlsx' in dir_list):
        print("Duplicate Found")
        file = 'tox_n_varition_Final.xlsx'
        location = "E:\PROECT_Main\LTspiceXVII\LTspiceXVII/" #done
        path1 = os.path.join(location, file)
        os.remove(path1)
    os.chdir(path)
    filename+=".xlsx"
    a=xlsxwriter.Workbook(filename)
    b=a.add_worksheet()
    b.write("A1","I_out(nA)")
    b.write("B1","tox values")
    for i in range(n):
        b.write(i+1,0,current[i])
        b.write(i+1,1,tox[i])
    a.close()

def vthxl(current,vtharray,filename,path,n):

    path1 = "E:\PROECT_Main\LTspiceXVII\LTspiceXVII"
    dir_list = os.listdir(path1)
    if('vth.xlsx' in dir_list):
        print("Duplicate Found")
        file = 'vth.xlsx'
        location = "E:\PROECT_Main\LTspiceXVII\LTspiceXVII" #done
        path1 = os.path.join(location, file)
        os.remove(path1)
    os.chdir(path)
    filename+=".xlsx"
    a=xlsxwriter.Workbook(filename)
    b=a.add_worksheet()
    b.write("A1","I_out(nA)")
    j=66
    for i in range(18):
        if i<9:
            h='vthen'+str(i+1)+'n'
            x=chr(j)+'1'
            b.write(x,h)
            j+=1 
        else:
            h='vthep'+str(i-8)+'p'
            x=chr(j)+'1'
            b.write(x,h)
            j+=1
    for i in range(n):
        b.write(i+1,0,current[i])
    k=1
    for arr in vtharray:
        for i in range(n):
            b.write(i+1,k,arr[i])
        k+=1
    a.close() 

def vthandtoxxl(current,vtharray,toxvalues,filename,path,n):

    path1 = "E:\PROECT_Main\LTspiceXVII\LTspiceXVII"
    dir_list = os.listdir(path1)
    if('toxvth.xlsx' in dir_list):
        print("Duplicate Found")
        file = 'toxvth.xlsx'
        location = "E:\PROECT_Main\LTspiceXVII\LTspiceXVII" #done
        path1 = os.path.join(location, file)
        os.remove(path1)
    os.chdir(path)
    filename+=".xlsx"
    a=xlsxwriter.Workbook(filename)
    b=a.add_worksheet()
    b.write("A1","I_out(nA)")
    b.write("B1","toxvalues")
    j=67
    for i in range(18):
        if i<9:
            h='vthen'+str(i+1)+'n'
            x=chr(j)+'1'
            b.write(x,h)
            j+=1 
        else:
            h='vthep'+str(i-8)+'p'
            x=chr(j)+'1'
            b.write(x,h)
            j+=1
    for i in range(n):
        b.write(i+1,0,current[i])
        b.write(i+1,1,toxvalues[i])
    k=2
    for arr in vtharray:
        for i in range(n):
            b.write(i+1,k,arr[i])
        k+=1
    a.close()

n=int(input('1:for tox variation \n2:for vth variation \n3:for tox and vth(both) \n4:for channel length \nplease enter a number(1 or 2 or 3 or 4)\n'))

if n!=1 and n!=2 and n!=3 and n!=4:
    print('enter a valid number')
if (n==1):
    sigma=float(input('Please enter the sigma value in percentage\n(for ex:for 3%,5%,7%... variation of vth just enter 3,5,7,..respectively )\n'))
    txtfile=input('Please enter the file in proper format including extension(.cir or .txt)\n')
    n1=int(input('Please enter number of variations:(How many values of tox you want to vary)\n'))
    filename=input('Please enter the csv file name\n')
    path=pathmodification(txtfile)
    toxvalues=m.toxvariation(sigma,txtfile,n1,path)
    d1=m.toxdisplay(path)
    print(d1)
    print('These are the variables to be plotted')
    a=int(input('enter the choice of x index you want to plot:'))
    b=int(input('enter the choice of y index you want to plot:'))
    l=m.toxplot(a,b,n1,path)
    for i in l:
        print(i)
    m,k,s =m.cal(l) 
    print("For Real Values : ")
    print("Mean value is: ",m)
    print("kurtosis value is: ",k)
    print("skewness value is: ",s)
    plot(l,n,n1)
    toxxl(l,toxvalues,filename,path,n1)
    df = pd.DataFrame(pd.read_excel(r"E:\PROECT_Main\VCO\measuremet\tox_n_varition_Final.csv")) ######need to be replaced
    custom_SVM(df)
if(n==2):
    sigma=float(input('Please enter the sigma value in percentage\n(for ex:for 3%,5%,7%... variation of vth just enter 3,5,7,..respectively )\n'))
    txtfile=input('Please enter the file in proper format including extension(.cir or .txt)\n')
    n3=int(input('Please enter the number of sample values\n'))
    filename=input('Please enter the csv file name\n')
    path=pathmodification(txtfile)
    d1=m.vthvariationdisplay(sigma,txtfile,n3,path)
    print(d1)
    print('These are the variables to be plotted')
    n1=int(input('enter the choice of x index you want to plot:'))
    n2=int(input('enter the choice of y index you want to plot:'))
    l,vthvalues=m.vthvariation(sigma,txtfile,n1,n2,n3,path)
    print('\n')
    for i in l:
        print(i)
    m,k,s=m.cal(l) 
    print("Mean value is: ",m)
    print("kurtosis value is: ",k)
    print("skewness value is: ",s)
    plt.hist(vthvalues,bins=n3)
    plt.xlabel('vth values')
    plt.ylabel('frequency')
    plt.title('Gaussian variation of vth')
    plt.show()
    plot(l,n,n3)
    vthxl(l,vthvalues,filename,path,n3)
    df = pd.DataFrame(pd.read_excel(r"E:\PROECT_Main\VCO\measuremet\VTH_n_varition_Final.csv")) #need to be changed
    X = df.drop('I_out(nA)', axis=1)
    y = df['I_out(nA)']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) #random_state=42
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.fit_transform(X_test)
    svr = SVR(C=0.1, gamma=0.01, kernel='rbf')
    svr.fit(X_train, y_train)
    y_pred = svr.predict(X_test)
    c=df['I_out(nA)']
    res=[]
    for mem in y_test:
        for i,mem1 in enumerate(c):
            if mem==mem1:
                res.append(df['vthen1n'][i])
    df = pd.DataFrame({'vthen1n':res, 'Real Values': y_test, 'Predicted Values':y_pred})
    print(df.to_string())
    mean=sum(y_pred)/len(y_pred)
    s=skew(y_pred)
    k=kurtosis(y_pred)
    print("For Predicted Values : ")
    print("Mean value is: ",mean)
    print("kurtosis value is: ",k)
    print("skewness value is: ",s)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)
if (n==3):
    sigma1=float(input('Please enter the sigma value for tox in percentage\n(for ex:for 3%,5%,7%... variation of vth just enter 3,5,7,..respectively )\n'))
    sigma2=float(input('Please enter the sigma value for vth in percentage\n(for ex:for 3%,5%,7%... variation of vth just enter 3,5,7,..respectively )\n'))
    txtfile=input('Please enter the file in proper format including extension(.cir or .txt)\n')
    n3=int(input('Please enter number of variations:(How many values of tox and vth you want to vary)\n'))
    filename=input('Please enter the csv file name\n')
    path=pathmodification(txtfile)
    d1=m.vthandtoxdisplayforuser(txtfile,sigma1,sigma2,n3,path)
    print(d1)
    print('These are the variables to be plotted')
    n1=int(input('Plese enter the choice of x index you want to plot:'))
    n2=int(input('Please enter the choice of y index you want to plot:'))
    l,vthvalues,toxvalues=m.variationforboth(txtfile,sigma1,sigma2,n1,n2,n3,path)
    print('\n')
    for i in l:
        print(i)
    m,k,s=m.cal(l) 
    print("Mean value is: ",m)
    print("kurtosis value is: ",k)
    print("skewness value is: ",s)
    plt.hist(toxvalues,bins=n3)
    plt.xlabel('tox values')
    plt.ylabel('frequency')
    plt.title('Gaussian variation of tox')
    plt.show()
    plt.hist(vthvalues,bins=n3)
    plt.xlabel('vth values')
    plt.ylabel('frequency')
    plt.title('Gaussian variation of vth')
    plt.show()
    plot(l,n,n3)
    vthandtoxxl(l,vthvalues,toxvalues,filename,path,n3)
    df = pd.DataFrame(pd.read_excel(r"E:\PROECT_Main\VCO\measuremet\VTH_P_varition_Final.csv")) ##need to change
    X = df.drop('I_out(nA)', axis=1)
    y = df['I_out(nA)']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.fit_transform(X_test)
    svr = SVR(C=0.1, gamma=0.01, kernel='rbf')
    svr.fit(X_train, y_train)
    y_pred = svr.predict(X_test)
    c=df['I_out(nA)']
    res1=[]
    res=[]
    for mem in y_test:
        for i,mem1 in enumerate(c):
            if mem==mem1:
                res1.append(df['vthen1n'][i])
                res.append(df['toxvalues'][i])
    df = pd.DataFrame({'Tox':res,'vthen1n':res1, 'Real Values': y_test, 'Predicted Values':y_pred})
    print(df.to_string())

    mean=sum(y_pred)/len(y_pred)
    s=skew(y_pred)
    k=kurtosis(y_pred)
    print("For Predicted Values : ")
    print("Mean value is: ",mean)
    print("kurtosis value is: ",k)
    print("skewness value is: ",s)
    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)
if(n==4):
    print("0: v1, 1: V(n002), 2: V(n001), 3: V(vdd), 4: V(n003), 5: V(vx), 6: V(n004), 7: V(n005), 8: V(n006), 9: Id(M11), 10: Ig(M11), 11: Ib(M11), 12: Is(M11), 13: Id(M10), 14: Ig(M10), 15: Ib(M10), 16: Is(M10), 17: Id(M9), 18: Ig(M9), 19: Ib(M9), 20: Is(M9), 21: Id(M7), 22: Ig(M7), 23: Ib(M7), 24: Is(M7), 25: Id(M8), 26: Ig(M8), 27: Ib(M8), 28: Is(M8), 29: Id(M6), 30: Ig(M6), 31: Ib(M6), 32: Is(M6), 33: Id(M5), 34: Ig(M5), 35: Ib(M5), 36: Is(M5), 37: Id(M4), 38: Ig(M4), 39: Ib(M4), 40: Is(M4), 41: Id(M3), 42: Ig(M3), 43: Ib(M3), 44: Is(M3), 45: Id(M2), 46: Ig(M2), 47: Ib(M2), 48: Is(M2), 49: Id(M1), 50: Ig(M1), 51: Ib(M1), 52: Is(M1), 53: I(V1)")
    print('These are the variables to be plotted')
    n1=int(input('Plese enter the choice of x index you want to plot:'))
    n2=int(input('Please enter the choice of y index you want to plot:'))
    res = chplot(n1,n2) 
    df = pd.DataFrame(pd.read_excel(r'C:\Users\sahar\OneDrive\Documents\LTspiceXVII\chl.xlsx'))
    m,k,s =m.cal(res) 
    print("For Real Values : ")
    print("Mean value is: ",m)
    print("kurtosis value is: ",k)
    print("skewness value is: ",s)
    X = df.iloc[:, 1].values
    y = df.iloc[:, -1].values

    from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    sc_y = StandardScaler()
    X = sc_X.fit_transform(X.reshape(-1, 1))
    y = sc_y.fit_transform(y.reshape(-1, 1))

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    from sklearn.svm import SVR
    regressor = SVR(C=0.1, gamma=0.01, kernel='rbf')
    regressor.fit(X_train.reshape(-1, 1), y_train.reshape(-1, 1))
    y_pred = regressor.predict(X_test.reshape(-1, 1))
    y_pred = sc_y.inverse_transform(y_pred.reshape(-1, 1))  
    z=sc_y.inverse_transform(y_test.reshape(-1, 1)).reshape(-1)
    I_values = df['I(A)']
    Vdd_values = []
    for i in range(len(z)):
        for j in range(len(I_values)):
            if z[i] == I_values[j]:
                Vdd_values.append(str(df['Channel Length'][j]))
                break
        else:
            Vdd_values.a
    df = pd.DataFrame({'Channel Length':Vdd_values, 'Real Values': sc_y.inverse_transform(y_test.reshape(-1, 1)).reshape(-1), 'Predicted Values': y_pred.reshape(-1)})
    print(df.to_string())
    mean = sum(y_pred) / len(y_pred)
    s = skew(y_pred)
    k = kurtosis(y_pred)
    print("For Predicted Values : ")
    print("Mean value is: ", mean)
    print("kurtosis value is: ", k)
    print("skewness value is: ", s)
    print('Mean Absolute Error is : ')
    print(metrics.mean_absolute_error(y_test, y_pred))
    print('Mean Squared Error is : ')
    print(metrics.mean_squared_error(y_test, y_pred))
    print('Root Mean Squared Error is :')
    print(np.sqrt(metrics.mean_squared_error(y_test, y_pred)))




