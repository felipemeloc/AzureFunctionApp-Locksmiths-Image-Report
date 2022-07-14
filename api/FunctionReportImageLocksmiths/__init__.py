import os
import sys
import logging
import azure.functions as func
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Define project main path
MAIN_FOLDER = os.getenv('MAIN_PATH')

sys.path.insert(0, os.path.join(os.getcwd(), os.path.join(MAIN_FOLDER, "src") ))

# from . import locksmiths_travel_report as tr



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        response = 'ALGO' # tr.locksmith_image()
        from . import locksmiths_travel_report as m
        response1 = m.locksmith_image()
        message = f"This HTTP triggered function executed successfully.\n\nResponse:\n{response1}"
        return  func.HttpResponse(message)
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(
             f"This HTTP triggered function FAIL successfully.\n\n{str(e)}",
             status_code=500
        )