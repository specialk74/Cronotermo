#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 18:58:42 2020

@author: marco
"""
import matplotlib
matplotlib.use('Agg')

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import base64
import io
import random

from datetime import datetime
from datetime import timedelta  
from pathlib import Path
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import HourLocator, MonthLocator, YearLocator

def ReadTodayFile(id, days = 0):
    now = datetime.now() - timedelta(days)  
    nomeFile = '/home/pi/data/'+str(id)+now.strftime("%Y")+now.strftime("%j")+'.csv'
    #newDict = dict(filter(lambda elem: elem[0] != 'id', req.items()))
    #print (newDict)
    output = pd.DataFrame()
    if os.path.exists(nomeFile) == True:
        output = pd.read_csv(nomeFile, parse_dates=["Data"])
    return output, nomeFile, now

def plot_temp():
    days = 1
    fig = plt.figure(figsize=[8,4])        

    samples, nomeFile, now = ReadTodayFile('Salone', days)
    if not samples.isin(['18363']).empty:
        x = samples['Data']
        y = samples['18363']
        plt.plot(x,y, label='Salone')

    samples, nomeFile, now = ReadTodayFile('Palestra', days)
    if not samples.isin(['2']).empty:        
        x = samples['Data']
        y = samples['2']
        plt.plot(x,y, label='Palestra')

    samples, nomeFile, now = ReadTodayFile('Cantina', days)    
    if not samples.isin(['11618']).empty:
        x = samples['Data']
        y = samples['11618']
        plt.plot(x,y, label='Cantina')

    title = 'Temperature - '

    plt.gca().xaxis.set_major_locator(HourLocator(byhour=None, interval=1, tz=None))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H'))

    plt.grid(which='minor', alpha=0.2)
    plt.grid(True)
    #df['Dates'] = pd.to_datetime(df['Dates'], format='%Y%m%d')
    plt.title(title+now.strftime("%Y/%m/%d"))
    plt.tick_params(labelright=True)
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.minorticks_on()

    for i in range(0, 100):
        y = random.randrange(100)
        x = random.randrange(60*24)
        plt.gca().text(x, y, "o", fontsize=15,  color='red')
            
    fig.savefig("Prova.png", format='png')
    
if __name__ == '__main__':
	plot_temp()
