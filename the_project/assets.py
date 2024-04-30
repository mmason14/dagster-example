from dagster import asset, OpExecutionContext
from pydexcom import Dexcom
import pandas as pd
import os
from datetime import datetime
from dagster_aws.s3.resources import s3_resource

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
def save_data(create_df, context: OpExecutionContext):
    df = create_df
    file_name = "daily_bg_readings.csv"
    bucket_name = os.environ.get("S3_BUCKET")
    bucket_location = context.resources.s3.get_bucket_location(Bucket=bucket_name)[
        "LocationConstraint"
    ]
    s3_path = f"https://s3.{bucket_location}.amazonaws.com/{bucket_name}/{file_name}"
    if os.path.isfile(s3_path) == False:
       context.resources.s3.upload_fileobj(bucket_name,  df.to_csv(s3_path, header=True))
    else:
        context.resources.s3.upload_fileobj(bucket_name, df.to_csv(s3_path, mode='a', header=False))



    
    
    