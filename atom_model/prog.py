import numpy as np
import pandas as pd
import os
from os.path import join as join
ion = 35009.8140

path=os.path.dirname(os.path.abspath(__file__) )

dat = np.loadtxt(join(path,'k1_nist.dat'),dtype = str)
kur = np.loadtxt(join(path,'kuruzc.dat'),dtype=str)
transitions = np.loadtxt(join(path,'list_of_transitions.dat'),dtype = str)



def main():
    name = dat[:,0]
    data = dat[:,1:].astype(float)

    levels_list = pd.DataFrame(columns = ['name','g','e'])  


    levels_list = levels(levels_list,name,data)

    levels_list.to_csv('atom_model/levels_list.dat',sep = '\t', index = False)

    lower_level = transitions[:,0]
    upper_level = transitions[:,1]

    loggf = kur[:,1].astype(float)
    j1 = kur[:,4].astype(float)
    name1_1 = kur[:,5]
    name1_2 = kur[:,6]
    name1=np.char.add(name1_1,name1_2)
    #print(name1)
    j2 = kur[:,8].astype(float)
    name2_1 = kur[:,9]
    name2_2 = kur[:,10]
    name2=np.char.add(name2_1,name2_2)
    kur_transitions = pd.DataFrame(columns = ['name1','name2','loggf','j1','j2'])

    kur_transitions = transitions1(kur_transitions,loggf, name1,name2,j1,j2,lower_level, upper_level)

    loggf = kur_transitions['loggf']
    f= 10**loggf 

    kur_transitions['f'] = f

    #kur_transitions.to_csv('f',float_format='%.5f',sep = '\t', index = False)
    kur_transitions.to_csv('atom_model/kur_transitions.dat',sep = '\t', index = False)
    '''
    for i in range(len(kur_transitions)-1):
     f= 10**loggf 
     #print ("%.4f" % f[i]) 

    kur_transitions['f'] = f
    print(kur_transitions)

    '''
    kur_final=pd.DataFrame(columns = ['name1','name2','f_total'])


    count_flag = False
    for i in range(len(kur_transitions)-1):
      for k in range(len(kur_transitions)-1):
            
        #for (i!=k):
         if count_flag:
             count_flag = False
             continue

            
         if i!=k:
            
          if all([name1[i]==name1[k],name2[i]==name2[k],name2[i]!=name2[i-2]]):
            #print(name1[i],name2[i])  

            
            count_flag = True

    for i in range(len(kur_transitions)-2):
        if all([name1[i]==name1[i+1],name2[i]==name2[i+1],name2[i]!=name2[i+2] or name1[i]!=name1[i+2] ]):
            ftot = ((2*j1[i]+1)*f[i]+(2*j1[i+1]+1)*f[i+1])/((2*j1[i]+1)+(2*j1[i+1]+1))
      #print(name1[i],name2[i],"%.4f" %ftot)
     # print(name1[i],"    ",name2[i],"     ","%.5f" %ftot)
            kur_final = kur_final.append({'name1':name1[i],'name2':name2[i],'f_total':ftot},ignore_index=True)

    for i in range(len(kur_transitions)-2):
        if all([name1[i]==name1[i+1],name2[i]==name2[i+1],name2[i]==name2[i+2]]):
            ftot = ((2*j1[i]+1)*f[i] + (2*j1[i]+1)*f[i+1] + (2*j1[i+2]+1)*f[i+2])/((2*j1[i]+1)+(2*j1[i+2]+1))
            kur_final = kur_final.append({'name1':name1[i],'name2':name2[i],'f_total':ftot},ignore_index=True)
      #print(name1[i],"    ",name2[i],"     ","%.5f" %ftot)

    for i in range(len(kur_transitions)-2):
        if all([name1[i]==name1[i+2],name2[i]==name2[i+2],name2[i]!=name2[i+1] or name1[i]!=name1[i+1]]):
            ftot = ((2*j1[i]+1)*f[i] + (2*j1[i]+1)*f[i] + (2*j1[i+2]+1)*f[i+2])/((2*j1[i]+1)+(2*j1[i+2]+1))
            kur_final = kur_final.append({'name1':name1[i],'name2':name2[i],'f_total':ftot},ignore_index=True)
           #print(name1[i],"    ",name2[i],"     ","%.5f" %ftot)


    kur_final.to_csv('atom_model/kur_final.dat',sep = '\t', index = False)


def levels(levels_list,name,data):
    count_flag = False
    for i in range(len(dat)-1):
        if count_flag:
            count_flag = False
            continue
        if name[i] == name[i+1]:
            #print(name[i])
            g_sum = (2*data[i,0]+1)+(2*data[i+1,0]+1)
            en=(((2*data[i,0]+1)*data[i,1]+(2*data[i+1,0]+1)*data[i+1,1])/((2*data[i,0]+1)+(2*data[i+1,0]+1)))
            levels_list = levels_list.append({'name':name[i],'g':g_sum,'e':en},ignore_index=True)
            count_flag = True
        else:
            levels_list = levels_list.append({'name':name[i],'g':2*data[i,0]+1,'e':data[i,1]},ignore_index=True)
    #print(levels_list)

    e = levels_list['e']
    #print(e)

    nu = 0.2997925*(ion - e)*100000000000
    #print(nu)
    levels_list['energy'] = nu
    #print(levels_list)
    del levels_list['e']
    #print(levels_list)

    return levels_list


def transitions1(kur_transitions,loggf, name1,name2,j1,j2,lower_level, upper_level):
    for i in range(len(kur)-1):
        for k in range(len(transitions)-1):   
            if all([name1[i]==lower_level[k],name2[i]==upper_level[k]]):
       
                kur_transitions = kur_transitions.append({'name1':name1[i],'name2':name2[i],'loggf':loggf[i],'j1':j1[i],'j2':j2[i]},ignore_index=True)
       #print(kur_transitions)
     #elif all([name1[i]==upper_level[k],name2[i]==lower_level[k]]):
           #print(name1[i],name2[i],gf[i],j1[i],g2[i])
     
    for i in range(len(kur)-1):
        for k in range(len(transitions)-1):
    
     #elif all([name1[i]==lower_level[k],name2[i]==upper_level[k]]):
            if all([name1[i]==upper_level[k],name2[i]==lower_level[k]]):
      
                kur_transitions = kur_transitions.append({'name1':name1[i],'name2':name2[i],'loggf':loggf[i],'j1':j1[i],'j2':j2[i]},ignore_index=True)
           #print(name1[i],name2[i],gf[i],j1[i],g2[i])


#print(kur_transitions)
#kur_transitions.to_csv('kur_transitions.dat',sep = '\t', index = False)

    return kur_transitions


if __name__=='__main__':
    main()


                                  
 

