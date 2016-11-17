
# coding: utf-8

# In[1]:

import pyaudio
import scipy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.legend_handler import HandlerLine2D
import numpy as np
import threading
import time, datetime
import math
import pandas as pd
from scipy.optimize import fsolve


bufferSize=2**11
sampleRate=44100
p = pyaudio.PyAudio()
Channel1=[]
Channel2=[]
data=[]
data1=[]


# In[2]:
##Variablen:

#Abstand vom Laptop zu den Punkten in m
V=0.5
#Abstand zwischen den Punkten in m
h=0.5
#Abstand der Mikrofone in m
A=0.5
#Grenzbereiche für die 5 Positionen
Grenzen = [0-(3/2)*h,0-h/2,0+h/2,0+(3/2)*h]
#Lautstärkepegel zur Aktivierung
Laut = 0.1


# In[3]:

def stream():
    global inStream, bufferSize, data1       
    N = max(inStream.get_read_available() / bufferSize, 1) * bufferSize * 8
    data1 = inStream.read(int(N))


# In[4]:

def record():
    global inStream, p, bufferSize
    inStream = p.open(format=pyaudio.paFloat32,channels=2,        rate=sampleRate,input=True,frames_per_buffer=bufferSize)


# In[5]:

def graph():
    global bufferSize, Channel1, Channel2, data, data1
    data = np.fromstring(data1, 'Float32')            
    Channel1 = data[0::2]
    Channel2 = data[1::2]


# In[6]:

def go(x=None):
    threading.Thread(target=record).start()


# In[7]:

def animate(i):
    global Channel1, Channel2, y, position, V, h, A, Grenzen, Laut, Delta
    stream()
    graph()
    ax[0].clear()
    ax[1].clear()
    
    #Plot 1 Anzeige
    p1, = ax[0].plot(range(0,len(Channel1)), Channel1, 'r', label='Channel 1')
    p2, = ax[0].plot(range(0,len(Channel2)), Channel2, 'b', label='Channel 2', alpha=0.6)
    first_legend = ax[0].legend(handler_map={p1: HandlerLine2D(numpoints=2)}, loc=1)
    ax[0].set_title('Darstellung der Soundeingaenge')
    ax[0].set_ylabel('Amplitude')
    
    #Plot 2 Korrelationsberechnung
    full=np.correlate(Channel1,Channel2,'full')
    mf=max(full)
    PandaData2=pd.DataFrame(data=full,columns=['Korrelation'])
    position=PandaData2[PandaData2['Korrelation']==mf].index[0]
    position=len(full)/2 - position + 0.0
    
    #Wegunterschied von Ton (mic1 zu mic2)
    Delta = (position/sampleRate)*343
    
    #Horizontaler Abstand des Soundursprungs zur Mitte der Mikrofone
    y = fsolve(lambda H : H*A-np.sqrt((H-A/2)**2+V**2)*Delta+Delta**2, 0)[0]
    
	#TestAnzeige für den Horizontalen Abstand y:
    #p3, = ax[1].plot(0,0,'g',label=y)
    #second_legend = ax[1].legend(handles=[p3], loc=2)
    
    #Bestimmung der Positionsanzeige
    if max(Channel1)<Laut:
        Farbe1 = 'r'
        Farbe2 = 'r'
        Farbe3 = 'r'
        Farbe4 = 'r'
        Farbe5 = 'r'
    elif y > Grenzen[3]:
        Farbe1 = 'r'
        Farbe2 = 'r'
        Farbe3 = 'r'
        Farbe4 = 'r'
        Farbe5 = 'g'
    elif y < Grenzen[0]:
        Farbe1 = 'g'
        Farbe2 = 'r'
        Farbe3 = 'r'
        Farbe4 = 'r'
        Farbe5 = 'r'
    elif Grenzen[0]<y<Grenzen[1]:
        Farbe1 = 'r'
        Farbe2 = 'g'
        Farbe3 = 'r'
        Farbe4 = 'r'
        Farbe5 = 'r'
    elif Grenzen[1]<y<Grenzen[2]:
        Farbe1 = 'r'
        Farbe2 = 'r'
        Farbe3 = 'g'
        Farbe4 = 'r'
        Farbe5 = 'r'
    elif Grenzen[2]<y<Grenzen[3]:
        Farbe1 = 'r'
        Farbe2 = 'r'
        Farbe3 = 'r'
        Farbe4 = 'g'
        Farbe5 = 'r'
    
    #Plot 2 Anzeige
    ax[1].scatter(1,1,s=3000,color=Farbe1)
    ax[1].scatter(2,1,s=3000,color=Farbe2)
    ax[1].scatter(3,1,s=3000,color=Farbe3)
    ax[1].scatter(4,1,s=3000,color=Farbe4)
    ax[1].scatter(5,1,s=3000,color=Farbe5)
    
    ax[1].axis([0,6,0,2])
    ax[1].axis('off')
    ax[1].set_title('Ursprung des Soundsignals')


# In[24]:

go()
fig1, ax = plt.subplots(2)
plt.subplots_adjust(hspace=1)
ani = animation.FuncAnimation(fig1, animate, interval=500)
plt.show()