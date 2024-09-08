import os
import sys
import pandas as pd
import math
import random
from sklearn.neighbors import KNeighborsClassifier
import time 
import numpy as np 
import plotext as plt 

def drawplot(dataframe):
    df=dataframe

    bream=df[df['ranswer']==1]
    smelt = df[df['ranswer']==0]

    bx=bream['length']
    by=bream['weight']

    sx=smelt['length']
    sy=smelt['weight']

    newx=df['length'].iloc[-1]
    newy=df['weight'].iloc[-1]

    plt.plotsize(40,10)
    plt.xlabel("length")
    plt.ylabel("weight")
    plt.scatter(bx,by,marker='B',color='red')
    plt.scatter(sx,sy,marker='S',color='blue')
    plt.scatter([newx], [newy], marker='*',color='green')
    plt.title("location of input data")
    plt.show()
    

def display_progress(percentage):
    bar_length = 50 
    filled_length = int(round(bar_length * percentage / 100))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    print(f'\r[{bar}] {percentage:.2f}%', end='')

def print_growth(answer_ratio):
    total_percentage = answer_ratio
    step = 5
    for i in range(0, total_percentage + step, step):
        display_progress(min(i, total_percentage))
        time.sleep(0.1) 
    display_progress(total_percentage)
    print(" ")    

def main():
    home_path = os.path.expanduser('~')
    data_path=f"{home_path}/data/GML/"
    file_path=f"{home_path}/data/GML/gml.csv"

    if os.path.exists(file_path):
        df=pd.read_csv(file_path) 
    else:
        df=pd.DataFrame(
            {
            'length' : [],
            'weight': [],
            'MLanswer' : [],
            'ranswer': [],
            }
        )

    length,weight= map(float, input("길이와 무게를 입력하세요:").split())

    if len(df) == 0:
        fanswer = random.randint(0,1)
        df.loc[len(df)] = [length,weight,fanswer,0]
        if fanswer==1.0:
            print("일단은 도미")
        else :
            print("일단은 빙어")
    
        answer=input("정답을 입력하세요(y or n) :")
        if answer == 'y':
            print("역시 그렇군요")
            df.loc[len(df)-1:len(df), "ranswer"] = fanswer
        else : 
            if fanswer == 1.0:
                df.loc[len(df)-1:len(df), "ranswer"] = 0
                print("강해져서 돌아오겠습니다")
            else :
                df.loc[len(df)-1:len(df), "ranswer"] = 1
                print("강해져서 돌아오겠습니다")
    
   
    else:
        kn=KNeighborsClassifier(n_neighbors=int((math.sqrt(len(df)))))
        kn.fit(df.iloc[:,0:2].values,df.loc[:,'ranswer'])
        pred=int(kn.predict([[length,weight]])[0])
        if  pred == 1.0:
            df.loc[len(df)] = [length,weight,pred,0]
            print("도미")
        else :
            df.loc[len(df)] = [length,weight,pred,0]
            print("빙어")
        answer=input("정답을 입력하세요(y or n):")
        if answer == 'y':
            print("역시 그렇군요")
            df.loc[len(df)-1:len(df), "ranswer"] = pred
        else : 
            if pred == 1.0:
                df.loc[len(df)-1:len(df), "ranswer"] = 0
                print("강해져서 돌아오겠습니다")
            else :
                df.loc[len(df)-1:len(df), "ranswer"] = 1
                print("강해져서 돌아오겠습니다")


    print("\n")
    print("[정답율]")
    print_growth(int((len(df[df['MLanswer']==df['ranswer']])/len(df))*100))
    print("[입력 데이터 위치]")
    drawplot(df)
    print("\n")
    os.makedirs(os.path.dirname(data_path), exist_ok = True)
    df.to_csv(file_path,index=False)








    
