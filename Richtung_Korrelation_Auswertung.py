
# coding: utf-8

# # Korrelation zwischen zwei Audio Kanälen berechnen zur Positionsbestimmung

# Imports:

# In[26]:

from scipy.io import wavfile
import numpy as np
import pandas as pd
import scipy as sc
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import math
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename


# Fenster erstellen fuer GUI

# In[27]:

fenster = tk.Tk()
fenster.title("Positionsbestimmung per Korrelation")
fenster.geometry("410x150");


# Abstand der Mikrofone festlegen

# In[28]:

lab1= tk.Label(fenster, text = 'Abstand der Mikrofone in m:')
lab1.pack()
eingabe = tk.Entry(fenster)
eingabe.insert(0, 0.056)
eingabe.pack()


# Ergebnisfeld definieren als globale Variable, damit bei erneuter Ausführung das alte Ergebnis gelöscht werden kann

# In[29]:

global lab
lab =tk.Label(fenster, text = 'Ergebnis_Platzhalter')


# Rahmenbedingungen für Knöpfe und einzulesende Dateien

# In[30]:

button_opt = {'fill': tk.constants.BOTH, 'padx': 5, 'pady': 5}

file_opt = options = {}
options['defaultextension'] = '.wav'
options['filetypes'] = [('all files', '.*'), ('sound files', '.wav')]
options['initialfile'] = 'ton.wav'
options['parent'] = fenster
options['title'] = 'Zu analysierende Ton Datein auswählen'


# Funktion zum Dateien einlesen:

# In[31]:

global filename
filename = 'ton.wav'

def openfilename():
    global filename
    filename = askopenfilename(**file_opt)


# Funktion zur Korrelationsberechnung und Anzeige der Ergebnisse:

# In[32]:

def ausgabe():
    global filename
    samplerate , Data = wavfile.read(filename) #Einlesen der wav-Daten gibt Samplerate und Datenarray mit Werten zwischen -32768 und +32768 zurück
    Data64=np.array(Data, dtype=np.int64) #Datentyp zu 64 bit Integer ändern, um bei der Korrelationsberechnung das richtige Maximum zu erreichen und nicht durch zu niedrige Werte begrenzt zu sein
    samplerate=samplerate+0.0 #Samplerate für spätere Rechnung in float konvertieren
    mikrofon = int(math.ceil((float(eingabe.get()))/343.2 * samplerate)) #maximaler zeitliche Differenz des linken und rechten Channels abhängig von dem Abstand der Mikrofone
    Channel1=[] #Daten in Listen schreiben
    Channel2=[]
    for i in Data64:
        Channel1.append(i[0])
        Channel2.append(i[1])
    full=np.correlate(Channel1,Channel2,'full') #Korrelation des linken und rechten Mikrofons berechnen - Beide Channel gegeneinander verschieben
    mf=max(full)
    PandaData2=pd.DataFrame(data=full,columns=['Korrelation'])
    position2=PandaData2[PandaData2['Korrelation']==mf].index[0] #Zeitverschiebung der maximalen Korrelation bestimmen - Verschiebung läuft jeweils von der Mitte der Liste ins positive und negative, also den Abstand zur Mitte der Liste benutzen
    position2=len(full)/2 - position2 + 0.0
    abstand2=position2/samplerate*343.2 #Wegdifferenz des Schalls zum linken und rechten Mikrofon (Schallgeschwindigkeit in trockener Luft 20°C - 343,2 m/s)
    #wenn Abstand größer 0, dann kommt der ton zuerst am linken mikrofon an und die Person steht links,...
    if abstand2 > 0.005:
        ergebnis= "Person steht links"
    elif abstand2 < -0.005:
        ergebnis= "Person steht rechts"
    else:
        ergebnis= "Person steht in der Mitte"
        
    global lab
    lab.destroy()
    lab= tk.Label(fenster, text = ergebnis) #Ergebnis in Textfeld ausgeben
    lab.pack()
        
        
    # Channel 1 und 2 in array schreiben um Position der Maxima zu bestimmen
    amplitude1 = np.array(Channel1)
    amplitude2 = np.array(Channel2)    
    amplitudelist1 = pd.DataFrame(data=amplitude1,columns=['Amplitude'])
    positionmax1=amplitudelist1[amplitudelist1['Amplitude']==max(Channel1)].index[0]
    # Bereich von Channel 2 auswählen der um das globale Max von Channel 1 liegt, um lokales Maximum von Channel 2 zu finden
    Channel3 =[]
    for i in range(positionmax1-mikrofon, positionmax1+mikrofon):
        Channel3.append(amplitude2[i])
    amplitudelist2 = pd.DataFrame(data=amplitude2,columns=['Amplitude'])
    # Aus Channel 2 alle Werte gleich dem lokalen Maximum außerhalb des zu betrachtenden Bereichs löschen, um diesen referieren zu können
    while amplitudelist2[amplitudelist2['Amplitude']==max(Channel3)].index[0] < positionmax1-mikrofon:
        amplitudelist2['Amplitude'][amplitudelist2[amplitudelist2['Amplitude']==max(Channel3)].index[0]]=0
    while amplitudelist2[amplitudelist2['Amplitude']==max(Channel3)].index[0] > positionmax1+mikrofon:
        amplitudelist2['Amplitude'][amplitudelist2[amplitudelist2['Amplitude']==max(Channel3)].index[0]]=0
    
    positionmax2=amplitudelist2[amplitudelist2['Amplitude']==max(Channel3)].index[0]
    
    ###############
    ##Plot erstellen
    #Channel Vergleichen
    f, ax = plt.subplots(2,2)
    f.canvas.set_window_title('Amplitudenvergleich und Korrelation') #Fenstertitel
    f.set_size_inches(14, 8, forward=True) #Fenstergröße in inches
    
    p1, = ax[0, 0].plot(range(1,len(Channel1)+1), Channel1, 'r', label='Channel 1')
    ax[0, 0].plot(range(1,len(Channel2)+1), Channel2, 'b', label='Channel 2')
    ax[0, 0].legend(handler_map={p1: HandlerLine2D(numpoints=2)}, loc=1)
    ax[0, 0].axis([0, len(Channel1)+0.0, min(Channel1)+0.0, max(Channel1)+0.0])
    ax[0, 0].set_title('Vergleich Channel 1 mit Channel 2')
    ax[0, 0].set_ylabel('Amplitude')

    p2, = ax[1, 0].plot(range(1,len(Channel1)+1), Channel1, 'r', label='Channel 1')
    ax[1, 0].plot(range(1,len(Channel2)+1), Channel2, 'b', label='Channel 2')
    #Abstandsanzeige [x1,x2],[y1,y2]
    ax[1, 0].plot([positionmax1+1, positionmax2+1], [max(Channel2), max(Channel2)], color='k', linestyle='-', linewidth=2)
    ax[1, 0].plot([positionmax1+1, positionmax1+1], [max(Channel2)-0.1*max(Channel2), max(Channel2)+0.1*max(Channel2)], color='k', linestyle='-', linewidth=2)
    ax[1, 0].plot([positionmax2+1, positionmax2+1], [max(Channel2)-0.1*max(Channel2), max(Channel2)+0.1*max(Channel2)], color='k', linestyle='-', linewidth=2)
    #Bedingungen für Textausrichtung
    if abstand2 > 0.005:
        z=positionmax1+1.1
    elif abstand2 < -0.005:
        z=positionmax2+1.1
    else:
        z=positionmax1+1
    abstandchannelmax = position2/samplerate*10000
    ax[1, 0].text(z, max(Channel2), 'Abstand: ' + str(round(abstandchannelmax, 2)) + ' $\cdot 10^{-4}$ s')
    ax[1, 0].legend(handler_map={p2: HandlerLine2D(numpoints=2)},loc=3)
    if abstand2 > 0.005:
        ax[1, 0].axis([positionmax1-mikrofon/2, positionmax1+2*mikrofon, max(Channel2)/2, max(Channel1)+0.0])
    elif abstand2 < -0.005:
        ax[1, 0].axis([positionmax1-2*mikrofon, positionmax1+mikrofon/2, max(Channel2)/2, max(Channel1)+0.0])
    else:
        ax[1, 0].axis([positionmax1-mikrofon, positionmax1+mikrofon, max(Channel2)/2, max(Channel1)+0.0])
    ax[1, 0].set_title('Hineingezoomt')
    ax[1, 0].set_xlabel('Zeit in $1/44100 \; s$')
    ax[1, 0].set_ylabel('Amplitude')
    
    
    korrlaenge = len(full)
    if korrlaenge % 2 == 0:
        korrlaenge1 = int(-korrlaenge/2)
        korrlaenge2 = int(korrlaenge/2)
    else:
        korrlaenge1 = int(-(korrlaenge + 1)/2)
        korrlaenge2 = int((korrlaenge - 1)/2)
    
    
    #Korrelationsbetrachtung
    p3, = ax[0, 1].plot(range(korrlaenge1,korrlaenge2), full, 'r', label='Korrelation')
    ax[0, 1].legend(handler_map={p3: HandlerLine2D(numpoints=1)}, loc=1)
    ax[0, 1].axis([korrlaenge1+0.0, korrlaenge2+0.0, min(full)+0.0, max(full)+0.0])
    ax[0, 1].set_title('Korrelation Channel 1 und Channel 2')
    ax[0, 1].set_ylabel('Korrelation')
    
    p4, = ax[1, 1].plot(range(korrlaenge1+1,korrlaenge2+1), full, 'r', label='Korrelation')
    ax[1, 1].legend(handler_map={p4: HandlerLine2D(numpoints=1)}, loc=1)
    #Abstandsanzeige
    ax[1, 1].plot([0, -1*position2], [max(full)-0.005*max(full)+0.0, max(full)-0.005*max(full)+0.0], color='k', linestyle='-', linewidth=2)
    ax[1, 1].plot([-1*position2, -1*position2], [max(full)-0.0055*max(full)+0.0, max(full)-0.0045*max(full)+0.0], color='k', linestyle='-', linewidth=2)
    ax[1, 1].plot([0, 0], [max(full)-0.0055*max(full)+0.0, max(full)-0.0045*max(full)+0.0], color='k', linestyle='-', linewidth=2)
    #Bedingungen für Textausrichtung
    if abstand2 > 0.005:
        z=-1*position2
    elif abstand2 < -0.005:
        z=0
    else:
        z=0
    abstandchannelmax = position2/samplerate*10000
    ax[1, 1].text(z, max(full)-0.005*max(full)+0.0, 'Abstand: ' + str(round(abstandchannelmax, 2)) + ' $\cdot 10^{-4}$ s')
    ax[1, 1].legend(handler_map={p4: HandlerLine2D(numpoints=2)},loc=1)
    #Achsen festlegen
    if abstand2 > 0.005:
        ax[1, 1].axis([0-position2*2, 0+position2, max(full)-0.01*max(full)+0.0, max(full)+0.0])
    elif abstand2 < -0.005:
        ax[1, 1].axis([0+position2, 0-position2*2, max(full)-0.01*max(full)+0.0, max(full)+0.0])
    else:
        ax[1, 1].axis([0-position2, 0+position2, max(full)-0.01*max(full)+0.0, max(full)+0.0])
        
    ax[1, 1].set_title('Hineingezoomt')
    ax[1, 1].set_xlabel('Zeit in $1/44100 \; s$')
    ax[1, 1].set_ylabel('Korrelation')
    
    
    
    
    
    
    
    plt.show()


# Weitere Elemente für die GUI:

# In[33]:

knopf1 = tk.Button(fenster, text='Datei auswählen', command=openfilename)
knopf1.pack(**button_opt)


# In[34]:

knopf = tk.Button(fenster, text="Analyse", command=ausgabe)
knopf.pack(**button_opt)


# In[35]:

separator = tk.Frame(height=2, bd=1, relief=tk.SUNKEN)
separator.pack(fill=tk.X, padx=5, pady=5)


# In[36]:

tk.mainloop()

