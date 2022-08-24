import os
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
from . import travel_sheet_report as ts_r
from .src import db
from .src import utils
from .src import azure_blob as blob
from dotenv import load_dotenv
import logging

# Load environment variables
#load_dotenv()
# Define project main path
MAIN_FOLDER = os.getenv('MAIN_PATH')
REPORT_IMAGE = os.getenv('REPORT_IMAGE')
CONTAINER = os.getenv('CONTAINER')


################################## Query Load #####################################

query_path = os.path.join(MAIN_FOLDER, 'queries')

TS_completed_jobs_by_locksmith = open(os.path.join(query_path,
                    'TS_completed_jobs_by_locksmith.sql'), 'r').read()

def get_completed_locksmith_report():
    average_stat = ts_r.summary_locksmiths()
    logging.debug('Raw dataframe')
    logging.debug(average_stat)
    completed_jobs = db.sql_to_df(TS_completed_jobs_by_locksmith)
    if not completed_jobs.empty:
        completed_jobs['Locksmith'] = utils.clean_locksmith_name(completed_jobs['Locksmith'])
        completed_jobs = completed_jobs.groupby('Locksmith', as_index=False).sum()
        report = completed_jobs.merge(average_stat, on='Locksmith', how='left')
        report['£ per mile'] = report['Revenue'] / report['Miles covered']
        logging.info(f'DataFrame with {report.shape[0]} rows')
        return report.sort_values(['Revenue', 'Jobs'], ascending=False)
    else:
        return pd.DataFrame()

def df_to_image(df:pd.DataFrame, money_cols:list=[], max_length:int=14)->None:    
    for col, col_type in zip(df.dtypes.index, df.dtypes):
        if col in money_cols:
            df[col] = df[col].astype(float).apply(lambda x: f'£{x:.01f}' if not np.isnan(x) else x)
        elif col_type == 'float64':
            df[col] = df[col].apply(lambda x: f'{x:.02f}' if not np.isnan(x) else x)
        elif col_type == 'object':
            df[col] = df[col].fillna('').astype(str).apply(lambda x: x[0:max_length])
    df.fillna('', inplace=True)
    fig =  ff.create_table(df)
    fig.update_layout(
        autosize=False,
        width=100*df.shape[1],
        height=20*df.shape[0],
        )
    local_path = f'/tmp/tmp_image.png'
    fig.write_image(local_path, scale=2)
    if blob.blob_exists(REPORT_IMAGE):
        blob.delete_blob(REPORT_IMAGE)
    blob.upload(local_file_name= local_path, 
                cloud_file_name= REPORT_IMAGE)


def locksmith_image():
    logging.info('Process started')
    try:
        report = get_completed_locksmith_report()
        if not report.empty:
            df_to_image(report, money_cols=['Revenue', '£ per mile'])
            logging.info('Image generated')
            return f"The image was generated. Check the {CONTAINER} container"
        else:
            logging.info('Empty DataFrame')
            return "Process successful. Not image to display"
    except Exception as e:
        logging.exception(e)
        return e