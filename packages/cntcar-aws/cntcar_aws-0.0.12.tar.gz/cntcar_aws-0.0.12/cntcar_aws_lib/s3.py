import boto3
import os
import datetime as dt
from .utils import handle_error

def list_files(bucket_name:str, s3_path:str):
    """List all files at a given S3 path.
    
    Parameters:
        bucket_name : str
            The name of the S3 bucket.
        s3_path : str
            The path within the S3 bucket.
    
    Returns:
        list: A list of file keys (paths) in the specified S3 path.
    """
    try:
        s3_client = boto3.client('s3')
        paginator = s3_client.get_paginator('list_objects_v2')
        result = []

        for page in paginator.paginate(Bucket=bucket_name, Prefix=s3_path):
            if 'Contents' in page:
                for obj in page['Contents']:
                    result.append(obj['Key']) if (obj['Key']).endswith('.csv') else None

        return result
    except Exception as e:
        detail = f'Error listing S3 files: {str(e)}'
        handle_error(e,detail)


def get_files(bucket:str, keys:list=None):
    """This function retrieves a file from an S3 bucket.
    
    Parameters:
        bucket : str
            The name of the S3 bucket where the file is stored.
        keys : list
            A list of keys of the files in the S3 bucket that needs to be retrieved.
    
    Return:
        list
    """
    try:
        s3 = boto3.client('s3')
        local_files = []
        for key in keys:
            local_file = '/tmp/' + os.path.basename(key)
            s3.download_file(bucket, key, local_file)
            local_files.append(local_file)
        if local_files: print(f'Files retrieved from S3 successfully - {dt.datetime.now()}')
        return local_files
    except Exception as e:
        detail = f'Error retrieving file from S3: {str(e)}'
        handle_error(e,detail)
    

def delete_files(bucket:str, keys:str):
    """This function deletes a file from an S3 bucket.
        
        Parameters:
            bucket : str
                The name of the S3 bucket where the file is stored.
            keys : list
                A list of keys of the files in the S3 bucket that needs to be deleted.
            
        Return:
            None
        """
    try:
        s3 = boto3.client('s3')
        for key in keys:
            s3.delete_object(Bucket=bucket, Key=key)
            print(f'File deleted from S3 successfully - {key} - {dt.datetime.now()}')
    except Exception as e:
        detail = f'Error deleting file from S3: {str(e)}'
        handle_error(e,detail)