"""azure_blob.py
This is a custom module to download azure files to
local or upload local files to azure
This module needs the installation of the following packages:
* os: For path management and directory creation
* dotenv: load environment variables
* azure.storage.blob:
Contains the following function:

* download: Function to download azure files to local. use:
    import azure_blob as blob
    blob.download(cloud_file_name= 'FILE_TO_BE_DOWLOAD',
                local_file_name= 'FILE_DOWLOAD_NAME')
    
* upload: Function to upload local files to azure. use:
    import azure_blob as blob
    blob.upload(local_file_name='FILE_TO_BE_UPLOAD',
                cloud_file_name='FINAL_UPLOAD_NAME')
"""

import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, _container_client

#load_dotenv()

BLOB_CONN_STR = os.getenv('BLOB_CONN_STR')
CONTAINER = os.getenv('CONTAINER')

def init_blob()->_container_client.ContainerClient:
    """Connection blob function, it is used to download azure files to
    local or upload local files to azure.

    Returns:
        _container_client.ContainerClient: Azure connection blob
    """
    blob = BlobServiceClient.from_connection_string(
        BLOB_CONN_STR
        ).get_container_client(
            CONTAINER
            )
    return blob

def blob_exists(blob_path:str)->bool:
    """Function to check if a file exists in Azure

    Args:
        blob_path (str): Path to an Azure file

    Returns:
        bool: Boolean if the file exists or not in Azure
    """    
    blob = init_blob()
    return blob.get_blob_client(blob_path).exists()

def download(cloud_file_name:str, local_file_name:str=None, as_bytes:bool=False):
    """Function to download azure files to local.
    It needs the target file

    Args:
        cloud_file_name (str): Target file in azure
        local_file_name (str, optional): The final path where
            the file will be after download. Defaults to None (same as target).
    """    
    blob = init_blob()
    if not local_file_name:
        local_file_name = cloud_file_name
    if blob_exists(cloud_file_name):
        blob_data = blob.download_blob(cloud_file_name)
        if as_bytes:
            return blob_data.content_as_bytes()
        else:
            with open(local_file_name, 'wb') as f:
                blob_data.readinto(f)
    
def upload(local_file_name:str, cloud_file_name:str=None):
    """Function to upload local files to azure.
    It needs the target file

    Args:
        local_file_name (str):Target file in local
        cloud_file_name (str, optional): The final path where
            the file will be after upload. Defaults to None (same as target).
    """
    blob = init_blob()
    if not cloud_file_name:
        cloud_file_name = local_file_name
    if os.path.exists(local_file_name):
        with open(local_file_name, 'rb') as f:
            blob.upload_blob(cloud_file_name, f)

def delete_blob(blob_path:str)->None:
    """Function to delete a Azure file

    Args:
        blob_path (str): Path to the blob to be deleted
    """
    blob = init_blob()
    if blob_exists(blob_path):
        blob.delete_blob(blob_path)