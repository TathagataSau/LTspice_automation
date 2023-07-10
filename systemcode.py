import random
import os
import matplotlib.pyplot as plt
import ltspy3
from scipy.stats import skew
from scipy.stats import kurtosis

def toxcal(s,n):
    list1=[]
    mu=4e-09
    sigma=(mu*s)/100
    for i in range(n):
        temp=random.gauss(mu,sigma)
        list1.append(temp)
    plt.hist(list1,bins=n)
    plt.xlabel('tox values')
    plt.ylabel('frequency')
    plt.title('Gaussian variation of tox')
    plt.show()
    command='.step param toxe list '
    command+=str(list1[0])
    for i in range(1,n):
        command+=','+str(list1[i])
    return command,list1
def toxcallimited(s,n):
    list1=[]
    mu=4e-09
    sigma=(s*mu)/100
    for i in range(n):
        temp=random.gauss(mu,sigma)
        list1.append(temp)
    return list1
def edittxtfortox(a,b,mypathTox):
    with open(a,'r') as f:
        r=f.readlines()
    for i in range(len(r)):
        if r[i]==".lib 'ts18sl_scl.lib' tt_18\n":
            s=i
            r[i]=".lib 'ts18sl_scl-toxVar.lib' tt_18\n"
    b=b+'\n'
    r.insert(s+1,b)
    u=''.join(r)
    myPathTox = mypathTox+'\\toxvariationall.txt'
    with open(myPathTox,'w') as f:
        f.write(u)
def automationfortox(path):
    location="C:\Program Files\LTC\LTspiceXVII"
    import subprocess
    path+='\\toxvariationall.txt'
    subprocess.call(location + "\XVIIx64.exe -Run "+path)
def toxvariation(sigma,txtfile,n,pathtox):  #in this function the corresponding functions for tox parameter will be called...
    x,list1=toxcal(sigma,n)
    edittxtfortox(txtfile,x,pathtox)
    automationfortox(pathtox)
    return list1
def display(name):
    l=list(i for i in range(len(name)))
    l1=[]
    for i in name:
        t=i.decode()
        l1.append(t)
    d1={}
    d1=dict(zip(l,l1))
    return d1
def toxdisplay(pathtox):
    filename="toxvariationall"
    pathtox+='\\toxvariationall.raw'
    sd=ltspy3.SimData(filename=pathtox)      #SimData is a tool that generates event data from a simulation of a user-defined scenario.
    name=sd.variables   #Here all the variables from sd file is stored in name file.
    freq_complex = sd.values    #Here all the values from the sd file is stored in freq_complex file.
    d1=display(name)
    return d1
def toxplot(n1, n2, n, pathtox):
    filename = "toxvariationall"
    pathtox += '\\toxvariationall.raw'
    sd = ltspy3.SimData(filename=pathtox)
    name = sd.variables
    freq_complex = sd.values
    a = sd.values[n1]
    b = sd.values[n2]
    for i in range(n):
        plt.plot(a[0], b[i])
    plt.xlabel('VDD (V)')
    plt.ylabel('I_out (nA)')
    plt.title('Power Supply Sensitivity for tox')
    v = len(a[0])
    x = None
    for j in range(v):
        if round(a[0][j], 2) >= 1.30:
            x = j
            break
    if x is not None:
        l = []
        for i in range(n):
            l.append(b[i][x])
        print(l)
        return l
    else:
        print("No value of x found.")
        return []        # List l is a replacement of measure command in Ltspice.It will store the current values
def cal(l):     
    if len(l) == 0:
        return None,None,None     #updated
    m=sum(l)/len(l)
    k=kurtosis(l)
    s=skew(l)
    return m,k,s
def vthcal(s,n):
    l=[0.38,0.41,0.39,0.5,0.43,0.39,0.45,0.42,0.38,0.45,0.37,0.42,0.43,0.43,0.40,0.41,0.42,0.40]
    j=0
    array=[]
    for i in range(18):
        list=[]
        sigma=(s*l[j])/100
        for i in range(n):
            temp=random.gauss(l[j],sigma)
            list.append(temp)
        j+=1
        array.append(list)
    return array  
def edittxtforvth(txtfile,add,myPathVth):
    with open(txtfile,'r') as file:
        readtxt=file.readlines()
    for i in range(len(readtxt)):
           if readtxt[i]==".lib 'ts18sl_scl.lib' tt_18\n":
               s=i
               readtxt[i]=".lib 'ts18sl_scl-vthVar1.lib' tt_18\n"
    m=len(readtxt)
    for i in add:
        i=i+'\n'
        readtxt.insert(m-2,i)
    edit=''.join(readtxt)
    myPathVth+='\\vthvariation1.txt'
    with open(myPathVth,'w') as file1:
         file1.write(edit)
def automationforvth(path):
    location="C:\Program Files\LTC\LTspiceXVII"
    import subprocess
    path+="\\vthvariation1.txt"
    subprocess.call(location + "\XVIIx64.exe -b "+path)
def vthdisplay(txtfile,array,path):
    for i in range(1):
        l=[]
        for j in range(18):
            if j<9:
                command='.param vthen'+str(j+1)+'n='
            else:
                command='.param vthep'+str(j-8)+'p='
            command+=str(array[j][i])   
            l.append(command)
        edittxtforvth(txtfile,l,path)
        automationforvth(path)
    filename="vthvariation1"
    path+="\\vthvariation1.raw"
    sd=ltspy3.SimData(filename=path)      #SimData is a tool that generates event data from a simulation of a user-defined scenario.
    name=sd.variables   #Here all the variables from sd file is stored in name file.
    freq_complex = sd.values    #Here all the values from the sd file is stored in freq_complex file.
    d1=display(name)
    return d1
def vthfinal(txtfile,array,n1,n2,n,path):
    l1=[]
    t=1
    c=0
    path1=path+"\\vthvariation1.raw"
    for i in range(n):
        l=[]
        for j in range(18):
            if j<9:
                command='.param vthen'+str(j+1)+'n='
            else:
                command='.param vthep'+str(j-8)+'p='
            command+=str(array[j][i])   
            l.append(command)
        edittxtforvth(txtfile,l,path)
        automationforvth(path)
        print(t,end="  ")
        t+=1
        filename="vthvariation1"
        sd=ltspy3.SimData(filename=path1)
        name=sd.variables
        freq_complex=sd.values
        a=sd.values[n1]
        b=sd.values[n2]
        if(c==0):
            v=len(a)
            for j in range(v):
                if round(a[j],2)>=1.20:
                    x=j
                    c=c+1
                    break
        l1.append(b[x])
        plt.plot(a,b)
    plt.xlabel('VDD(V)')  
    plt.ylabel('I_out(nA)')
    plt.title('Power supply sensitivity for different vth')
    plt.show()
    return l1
def vthvariationdisplay(sigma,txtfile,n,path):
    array=vthcal(sigma,n)
    d1=vthdisplay(txtfile,array,path)
    return d1
def vthvariation(sigma,txtfile,n1,n2,n,path):
    array=vthcal(sigma,n)
    l1=vthfinal(txtfile,array,n1,n2,n,path)
    return l1,array
def edit(txtfile,add,myPathToxVth):
    with open(txtfile,'r') as file:
        readtxt=file.readlines()
    for i in range(len(readtxt)):
           if readtxt[i]==".lib 'ts18sl_scl.lib' tt_18\n":
               s=i
               readtxt[i]=".lib 'ts18sl_scl-toxvthVar1.lib' tt_18\n"
    m=len(readtxt)
    for i in add:
        i=i+'\n'
        readtxt.insert(m-2,i)
    edit=''.join(readtxt)  
    myPathToxVth+='\\vthandtoxvariation1.txt'
    with open(myPathToxVth,'w') as file1:
        file1.write(edit)
def automation(path):
    location="C:\Program Files\LTC\LTspiceXVII"
    import subprocess
    path+='\\vthandtoxvariation1.txt'
    subprocess.call(location + "\XVIIx64.exe -b "+path)
def vthandtoxdisplay(txtfile,array,toxarray,path):
    path1=path+'\\vthandtoxvariation1.raw'
    for i in range(1):
        l=[]
        for j in range(18):
            if j<9:
                command='.param vthen'+str(j+1)+'n='
            else:
                command='.param vthep'+str(j-8)+'p='
            command+=str(array[j][i])   
            l.append(command)
        toxcommand='.param toxe='+str(toxarray[0])
        l.append(toxcommand)
        edit(txtfile,l,path)
        automation(path)
    filename="vthandtoxvariation1"
    sd=ltspy3.SimData(filename=path1)      #SimData is a tool that generates event data from a simulation of a user-defined scenario.
    name=sd.variables   #Here all the variables from sd file is stored in name file.
    freq_complex = sd.values    #Here all the values from the sd file is stored in freq_complex file.
    d1=display(name)
    return d1
def bothvariation(txtfile,vtharray,toxarray,n1,n2,n,path):
    l1=[]
    t=1
    c=0
    path1=path+'\\vthandtoxvariation1.raw'
    for i in range(n):
        l=[]
        for j in range(18):
            if j<9:
                command='.param vthen'+str(j+1)+'n='
            else:
                command='.param vthep'+str(j-8)+'p='
            command+=str(vtharray[j][i])   
            l.append(command)
        toxcommand='.param toxe='+str(toxarray[i])
        l.append(toxcommand)
        edit(txtfile,l,path)
        automation(path)
        print(t,end="  ")
        t+=1
        filename="vthandtoxvariation1"
        sd=ltspy3.SimData(filename=path1)
        name=sd.variables
        freq_complex=sd.values
        a=sd.values[n1]
        b=sd.values[n2]
        if(c==0):
            v=len(a)
            for j in range(v):
                if round(a[j],2)>=1.20:
                    x=j
                    c=c+1
                    break
        l1.append(b[x])
        plt.plot(a,b)
    plt.xlabel('VDD(V)')
    plt.ylabel('I_out(nA)')
    plt.title('Power supply sensitivity for vth and tox values')
    plt.show()
    return l1
def vthandtoxdisplayforuser(txtfile,sigma1,sigma2,n,path):
    toxvalues=toxcallimited(sigma1,n)
    vtharray=vthcal(sigma2,n)
    d1=vthandtoxdisplay(txtfile,vtharray,toxvalues,path)
    return d1
def variationforboth(txtfile,sigma1,sigma2,n1,n2,n,path):
    toxvalues=toxcallimited(sigma1,n)
    vtharray=vthcal(sigma2,n)
    l1=bothvariation(txtfile,vtharray,toxvalues,n1,n2,n,path)
    return l1,vtharray,toxvalues
