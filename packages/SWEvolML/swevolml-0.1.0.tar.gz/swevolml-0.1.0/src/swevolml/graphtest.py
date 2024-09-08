import pandas as pd 
import termplotlib as tpl
import numpy as np
import plotext as plt

df=pd.read_csv("~/data/GML/gml.csv")

bream=df[df['ranswer']==1]
smelt = df[df['ranswer']==0]

bx=bream['length']
by=bream['weight']

sx=smelt['length']
sy=smelt['weight']

newx=df['length'].iloc[-1]
newy=df['weight'].iloc[-1]

plt.plotsize(60,20)
plt.xlabel("length")
plt.ylabel("weight")
plt.scatter(bx,by,marker='B',color='red')
plt.scatter(sx,sy,marker='S',color='blue')
plt.scatter([newx], [newy], marker='*',color='green')
plt.title("location of input data")
plt.show()
