#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 18:58:42 2020

@author: marco
"""
import matplotlib
matplotlib.use('Agg')

import flask
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import base64
import io
import random

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from datetime import datetime
from datetime import timedelta  
from pathlib import Path
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, send_file, make_response, request 
from matplotlib.dates import HourLocator, MonthLocator, YearLocator

app = flask.Flask(__name__)
port = int(os.getenv("PORT", 9099))

x = np.arange(0, 128, 1)

# Ho preso la curva e gli ho sottratto il valore minore a tutti i valori
y = [0,0,0.009999999999998,0,0.009999999999998,0.009999999999998,0.009999999999998,0.009999999999998,0.02,0.029999999999998,0.039999999999999,0.029999999999998,0.029999999999998,0.02,0.009999999999998,0.009999999999998,0,0.009999999999998,0.029999999999998,0.029999999999998,0.039999999999999,0.039999999999999,0.059999999999999,0.069999999999997,0.079999999999998,0.09,0.109999999999999,0.119999999999997,0.129999999999999,0.129999999999999,0.149999999999999,0.159999999999997,0.169999999999998,0.169999999999998,0.18,0.199999999999999,0.199999999999999,0.219999999999999,0.219999999999999,0.229999999999997,0.239999999999998,0.25,0.25,0.27,0.279999999999998,0.299999999999997,0.309999999999999,0.319999999999997,0.329999999999998,0.349999999999998,0.349999999999998,0.369999999999997,0.379999999999999,0.389999999999997,0.389999999999997,0.409999999999997,0.419999999999998,0.43,0.439999999999998,0.449999999999999,0.459999999999997,0.459999999999997,0.479999999999997,0.489999999999998,0.489999999999998,0.5,0.5,0.509999999999998,0.509999999999998,0.52,0.529999999999998,0.529999999999998,0.539999999999999,0.539999999999999,0.549999999999997,0.559999999999999,0.559999999999999,0.559999999999999,0.559999999999999,0.579999999999998,0.569999999999997,0.579999999999998,0.59,0.59,0.59,0.59,0.599999999999998,0.599999999999998,0.609999999999999,0.609999999999999,0.609999999999999,0.619999999999997,0.619999999999997,0.619999999999997,0.619999999999997,0.629999999999999,0.629999999999999,0.629999999999999,0.639999999999997,0.649999999999999,0.649999999999999,0.659999999999997,0.659999999999997,0.669999999999998,0.68,0.68,0.689999999999998,0.699999999999999,0.699999999999999,0.709999999999997,0.709999999999997,0.719999999999999,0.729999999999997,0.729999999999997,0.739999999999998,0.75,0.759999999999998,0.77,0.77,0.779999999999998,0.779999999999998,0.789999999999999,0.799999999999997,0.809999999999999,0.809999999999999,0.809999999999999,0.819999999999997,0.829999999999998,]


df = pd.DataFrame()
df['Independent Variable'] = x
df['Dependent Variable'] = y

lm = LinearRegression()
X = np.asanyarray(df[['Independent Variable']])
Y = np.asanyarray(df[['Dependent Variable']])
lm.fit(X, Y)


@app.route('/predict', methods=['POST'])
def predict():
    features = flask.request.get_json(force=True)['value']
    token = flask.request.get_json(force=True)['token']
    prediction = (([features] - lm.intercept_) / lm.coef_)[0,0]
    #print(f'features: {features} - token: {token} - lm.intercept_: {lm.intercept_} - lm.coef_: {lm.coef_} - prediction: {prediction}')
    response = {'prediction': prediction}

    return flask.jsonify(response)

@app.route('/data', methods=['POST'])
def data():
    token = flask.request.get_json(force=True)['token']
    value = flask.request.get_json(force=True)['value']
    print('\tdata\tvalue: '+str(value[0])+' - token: '+str(token))
    
    response = {'result': 'OK!'}
    with open(str(token)+'.csv', 'a+') as file:  # Use file to refer to the file objct
        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
        file.write(dt_string+';'+str(value[0])+'\n')
        
    return flask.jsonify(response)

@app.route('/data2', methods=['POST'])
def data2():
    token = flask.request.get_json(force=True)['token']
    value = flask.request.get_json(force=True)['value']
    print('\tdata2\tflask.request.data\t'+str(flask.request.data))

    req = flask.request.get_json(force=True)
    print('\tdata2\tflask.request.get_json\t'+str(req))
    print('\tdata2\tflask.request.args\t'+str(flask.request.args))
    print('\tdata2\tflask.request.form\t'+str(flask.request.form))
    print('\tdata2\tflask.request.files\t'+str(flask.request.files))
    print('\tdata2\tflask.request.json\t'+str(flask.request.json))
    print('\tdata2\tvalue: '+str(value[0])+' - token: '+str(token))
    print('\tdata2\tIp Address: '+str(flask.request.remote_addr))
    
    if os.path.exists('data.csv') == False:
        with open('data.csv', 'a+') as file:  # Use file to refer to the file objct
            file.write('data');
            for val in req:
                if 'token' in val:
                    file.write(';'+str(val['token']))
            file.write('\n');
            
    print('\tval[\'token\']:'+str(val['token']))
    print('\tval[\'value\']:'+str(val['value']))
    with open('data.csv', 'a+') as file:  # Use file to refer to the file objct
        # datetime object containing current date and time
        now = datetime.now()
        #dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
        file.write(now.strftime("%Y/%m/%d %H:%M:%S"))
        for val in req:
            #print('\ttype(val): '+ str(type(val)))
            if 'value' in val:
                file.write(';'+str(val['value']))
        file.write('\n');

    response = {'result': 'OK!'}
        
    return flask.jsonify(response)

def ReadTodayFile(id, days = 0):
    now = datetime.now() - timedelta(days)  
    nomeFile = '/home/pi/data/'+str(id)+now.strftime("%Y")+now.strftime("%j")+'.csv'
    #newDict = dict(filter(lambda elem: elem[0] != 'id', req.items()))
    #print (newDict)
    output = pd.DataFrame()
    if os.path.exists(nomeFile) == True:
        output = pd.read_csv(nomeFile, parse_dates=["Data"])
    return output, nomeFile, now

@app.route('/data3', methods=['POST'])
def data3():
    #print('\tdata3\tflask.request.data\t'+str(flask.request.data))
    #token = flask.request.get_json(force=True)['token']
    #value = flask.request.get_json(force=True)['value']
    #print('\tdata3\tvalue: '+str(value[0])+' - token: '+str(token))

    req = flask.request.get_json(force=True)
    #print('\tdata3\tflask.request.get_json\t'+str(req))
    #print('\tdata3\tflask.request.args\t'+str(flask.request.args))
    #print('\tdata3\tflask.request.form\t'+str(flask.request.form))
    #print('\tdata3\tflask.request.files\t'+str(flask.request.files))
    #print('\tdata3\tflask.request.json\t'+str(flask.request.json))
    #print('\tdata3\tIp Address: '+str(flask.request.remote_addr))
    #print ('\treq[\'id\']:' + req['id'])
    
    #now = datetime.now()
    #nomeFile = '/home/pi/data/'+str(req['id'])+now.strftime("%Y")+now.strftime("%j")+'.csv'
    #newDict = dict(filter(lambda elem: elem[0] != 'id', req.items()))
    ##print (newDict)
    #output = pd.DataFrame()
    #if os.path.exists(nomeFile) == True:
    #    output = pd.read_csv(nomeFile, parse_dates=True)
    
    output, nomeFile, now = ReadTodayFile(req['id'])
    newDict = dict(filter(lambda elem: elem[0] != 'id', req.items()))
    
    newDict['Data'] = now.strftime("%Y/%m/%d %H:%M")
    output = output.append(newDict, ignore_index=True)
    output.to_csv(nomeFile, index=False)
    
    response = {'result': 'OK!'}
        
    return flask.jsonify(response)

@app.route('/data4', methods=['POST'])
def data4():
    token = flask.request.get_json(force=True)['token']
    value = flask.request.get_json(force=True)['value']
    print('\tdata4\tflask.request.data\t'+str(flask.request.data))

    req = flask.request.get_json(force=True)
    print('\tdata4\tflask.request.get_json\t'+str(req))
    print('\tdata4\tflask.request.args\t'+str(flask.request.args))
    print('\tdata4\tflask.request.form\t'+str(flask.request.form))
    print('\tdata4\tflask.request.files\t'+str(flask.request.files))
    print('\tdata4\tflask.request.json\t'+str(flask.request.json))
    print('\tdata4\tvalue: '+str(value[0])+' - token: '+str(token))
    print('\tdata4\tIp Address: '+str(flask.request.remote_addr))
    print ('\treq[\'id\']:' + req['id'])
    nomeFile = str(req['id'])+'.csv'
    newDict = dict(filter(lambda elem: elem[0] != 'id', req.items()))
    print (newDict)
    if os.path.exists(nomeFile) == False:
        with open(nomeFile, 'a+') as file:  # Use file to refer to the file objct
            file.write('data');
            for x in newDict.keys():
                file.write(';'+str(x))
            file.write('\n');
    with open(nomeFile, 'a+') as file:  # Use file to refer to the file objct
        # datetime object containing current date and time
        now = datetime.now()
        #dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
        file.write(now.strftime("%Y/%m/%d %H:%M"))
        for x in newDict.values():
            #print('\tx: '+ x)
            file.write(';'+str(x))
        file.write('\n');
    response = {'result': 'OK!'}
        
    return flask.jsonify(response)    

html = '''
<html>
    <body>
        <img src="data:image/png;base64,{}" />
    </body>
</html>
'''

@app.route('/plot', methods=['GET'])
def plot_temp():
    days = 0
    if 'days' in request.args:
        days = int(request.args.get('days')) #if key doesn't exist, returns None

    if 'watt' in request.args:
        fig = plt.figure(figsize=[20,20])

        samples, nomeFile, now = ReadTodayFile('Palestra', days)
        plt.subplot(2, 1, 1) #two rows, one columns, first graph
        samples['1084227584'].plot(label='Watt-h', legend=True, grid=True)
        samples['watt'] = samples['1084227584'] / 60
        plt.subplot(2, 1, 2) #two rows, one columns, first graph
        samples['watt'].plot(label='Watt', legend=True, grid=True)
        title = 'Watt - '
    else:
        fig = plt.figure(figsize=[20,10])        

        samples, nomeFile, now = ReadTodayFile('Salone', days)
        if not samples.isin(['18363']).empty:
            x = samples['Data']
            y = samples['18363']
            plt.plot(x,y, label='Salone')
            #samples['18363'].plot(grid=True, label='Salone', legend=True)
            
        #ax = samples['18363'].plot(label='Salone', legend=True)
        
        samples, nomeFile, now = ReadTodayFile('Palestra', days)
        if not samples.isin(['2']).empty:        
            #samples.plot(grid=True, label='Palestra', legend=True)
            x = samples['Data']
            y = samples['2']
            plt.plot(x,y, label='Palestra')
        
        samples, nomeFile, now = ReadTodayFile('Cantina', days)    
        if not samples.isin(['11618']).empty:
            x = samples['Data']
            y = samples['11618']
            plt.plot(x,y, label='Cantina')
            

            #samples['11618'].plot(grid=True, label='Cantina', legend=True)
            #samples.plot(x='Data', y='11618', grid=True, label='Cantina', legend=True)
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

    pngImage = io.BytesIO()
    fig.savefig(pngImage, format='png')
    pngImageB64String = base64.b64encode(pngImage.getvalue()).decode('utf8')
    
    return html.format(pngImageB64String)

if __name__ == '__main__':
    Path("/home/pi/data").mkdir(parents=True, exist_ok=True)
    app.run(host='0.0.0.0', port=port, threaded=True)