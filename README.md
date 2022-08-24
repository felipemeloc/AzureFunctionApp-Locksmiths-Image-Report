
path = 'api\FunctionReportImageLocksmiths\load_env.py'
```
import os

env_vars = {
# Project folder
'MAIN_PATH' : '',

# Roedan API
'EMAIL' : "",
'PASSWORD' : "",
'AUTHENTICATION_URL' : "",
'TRAVEL_SHEET_REPORT_URL' : "",

# Azure Blob
'BLOB_CONN_STR' : "",
'CONTAINER' : "",
'REPORT_IMAGE' : '',

# Database
'SERVER' : '',
'DATABASE' : '',
'USER_NAME' : '',
'DATABASE_PASSWORD' : ''

}

def load_env():
    for key, val in env_vars.items():
        os.environ[key] = val

load_env()
```