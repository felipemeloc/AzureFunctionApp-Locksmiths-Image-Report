import os
import pandas as pd
import requests
from datetime import timedelta
from .src import get_devices
from .src import api_authentication
from . import read_api_report_response as api_r
from dotenv import load_dotenv
import logging


load_dotenv()

USER_API_HASH = api_authentication.authentication()['USER_API_HASH']

################################## Basic paths #####################################

def get_devices_ids():
    response = get_devices.get_devices()
    status_code= response['status_code']
    if  status_code== 200:
        df = response['devices']
        df = df[df['group_name']== 'WGTK']
        return list(df['device_id'].astype(str).unique())
    else:
        message = response['message']
        process = response['process']
        raise Exception(f'{process}: STATUS CODE {status_code}, {message}')
    
def get_travel_sheet_report(date_from, date_to):
    arguments= {'user_api_hash': USER_API_HASH,
                    'lang': 'en',
                    'format': 'html',  # "html", "xls", "pdf", "pdf_land"
                    'type': 39, # Travel sheet custom
                    'date_from': date_from,
                    'date_to': date_to,
                    'devices':  get_devices_ids(),
                    'stops': 3*60 # 3 minutes * 60 seconds // number of seconds
                    }
    TRAVEL_SHEET_REPORT_URL =  os.getenv('TRAVEL_SHEET_REPORT_URL')
    api_response = requests.post(TRAVEL_SHEET_REPORT_URL, json = arguments)
    status_code = api_response.status_code
    message = None
    report_url = None
    logging.info(f'GENERATE TRAVEL REPORT: STATUS CODE {status_code}')
    if status_code == 200:
        report_url = api_response.json()['url']
        
    else:
        message = api_response.json()['message']
        logging.error(f'\tERROR: {message}')
        
    return {'status_code': status_code,
            'url':  report_url,
            'message': message,
            'process': 'GENERATE TRAVEL REPORT'}

def summary_locksmiths(date:pd.Timestamp=None):
    if not date:
        date = pd.Timestamp.now(tz="Europe/London")
    date_from= date.strftime('%Y-%m-%d') + ' 00:00:00'
    date_to= (date + pd.Timedelta(1, unit='d')).strftime('%Y-%m-%d') + ' 00:00:00'
    report_response = get_travel_sheet_report(date_from, date_to)
    url = report_response['url']
    df = api_r.get_full_response_table(url)
    average_stat = df.groupby('Locksmith', as_index=False).agg(
        {'Duration': 'sum',
        'Time at location': 'sum',
        'Route length (Mi)': 'sum'}
        ).rename(
            columns={'Duration': 'Driving time',
            'Time at location': 'Stop time',
            'Route length (Mi)': 'Miles covered'}
        ).sort_values('Miles covered', ascending=False)

    delta_str = lambda x: f"{timedelta(seconds=x.total_seconds())}"
    for col in ['Driving time', 'Stop time']:
        average_stat[col] = average_stat[col].apply(delta_str)
    
    return average_stat