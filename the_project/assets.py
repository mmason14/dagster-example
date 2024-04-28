from dagster import asset
from pydexcom import Dexcom
import pandas as pd
import os
from datetime import datetime

username = os.getenv("username")
password = os.getenv("password")

#print(username)
#print(password)


dexcom = Dexcom(username, password)





@asset
def get_current_bg():
    print(dexcom)
    return dexcom.get_current_glucose_reading()
   

@asset 
def create_df(get_current_bg):
    glucose_reading = get_current_bg
    if glucose_reading == None: 
        data = {'date': [datetime.now()], 'blood_glucose': ['No Data'],
                'trend': ['No Data'], 'trend_description': ['No Data']}
    else:
        data = {'date': [glucose_reading.datetime], 'blood_glucose': [glucose_reading],
        'trend': [glucose_reading.trend], 'trend_description': [glucose_reading.trend_description]}
    return pd.DataFrame(data=data)
        



@asset 
def save_data(create_df):
    df = create_df
    path = 'daily_bg_readings.csv'
    if os.path.isfile(path) == False:
        df.to_csv('daily_bg_readings.csv', header=True)
    else:
        df.to_csv('daily_bg_readings.csv', mode='a', header=False)

