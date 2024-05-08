from dagster import asset, OpExecutionContext
from pydexcom import Dexcom
import pandas as pd
import os
from datetime import datetime
from dagster_aws.s3.resources import s3_resource
import boto3
from io import StringIO
    

username = os.getenv("username")
password = os.getenv("password")




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
        



@asset(required_resource_keys={"s3", "io_manager"}) 
def save_data(context: OpExecutionContext, create_df):
    df = create_df
    csv_buffer=StringIO()
    df.to_csv(csv_buffer)
    content = csv_buffer.getvalue()
    
    file_name = "daily_bg_readings.csv"
    bucket_name = os.environ.get("S3_BUCKET")
    bucket_location = context.resources.s3.get_bucket_location(Bucket=bucket_name)[
        "LocationConstraint"
    ]

    bucket = "dexcom-data"
    folder = "daily_bg_readings"
    filename = "test"
    key = f"{folder}/{filename}"

    context.resources.s3.put_object(Bucket=bucket, Body=content,Key=key)

  