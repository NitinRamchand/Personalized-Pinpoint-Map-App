#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 12:41:57 2024

@author: nitin.ramchand-lalwani
"""

import os
import pandas as pd
from flask import Flask, render_template
from dotenv import load_dotenv
import json
import re

load_dotenv(dotenv_path='google_maps_api_key.env', verbose=True)

class Location:
    def __init__(self, latitude, longitude, business_name, complete_address, business_phone_number, business_email_address, cico_business_types_, total_transactions):
        self.lat = latitude
        self.lon = longitude
        self.nome = business_name
        self.complete_address = complete_address
        self.business_phone_number = business_phone_number
        self.business_email_address = business_email_address
        self.cico_business_types_ = cico_business_types_
        self.total_transactions = total_transactions

def read_data_from_df(df):
    lista = []
    for index, row in df.iterrows():
        lista.append(Location(row['latitude'], row['longitude'], row['business_name'], row['complete_address'], row['business_phone_number'], row['business_email_address'], row['cico_business_types_'], row['total_transactions']))
    return lista

app = Flask(__name__)
app.config['API_KEY'] = os.getenv("APIKEY")  # load google maps api key

def read_dataset(dataset):
    items = []
    for i in dataset:
        items.append([i.lat, i.lon, i.nome, i.complete_address, i.business_phone_number, i.business_email_address, i.cico_business_types_, i.total_transactions])
    return items


# Assuming df_test is your pandas DataFrame
df_test = pd.read_csv('df_final_cleaned_filtered_transactions.csv')

df_test['latitude'] = df_test['latitude'].astype(float)
df_test['longitude'] = df_test['longitude'].astype(float)

df_test['business_name'].fillna('')
df_test['business_name'] = df_test['business_name'].astype(str)


df_test['complete_address'].fillna('')
df_test['complete_address'] = df_test['complete_address'].astype(str)

df_test['business_phone_number'].fillna(0)
df_test['business_phone_number'] = df_test['business_phone_number'].astype(int)


df_test['business_email_address'].fillna('')
df_test['business_email_address'] = df_test['business_email_address'].astype(str)

df_test['total_transactions'].fillna(0)
df_test['total_transactions'] = df_test['total_transactions'].astype(int)
#df_test = df_test.iloc[:5000]
poidata = read_dataset(read_data_from_df(df_test))

@app.route('/')
def index():
    context = {
        "key": app.config['API_KEY'],
        "poidata": json.dumps(poidata)
    }
    return render_template('./index.html', poidata=poidata, context=context)

if __name__ == '__main__':
    app.run(debug=False)