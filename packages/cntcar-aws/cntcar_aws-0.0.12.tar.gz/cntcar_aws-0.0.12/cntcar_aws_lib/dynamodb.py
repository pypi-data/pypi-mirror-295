import boto3
import datetime as dt
from .utils import handle_error

def get_table_keys(table_name:str):
    '''This function retrieves the primary key attributes from a DynamoDB table.
    
    Parameters:
        table_name : str
            The name of the DynamoDB table.
    
    Return:
        str
    '''
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        pkey = table.key_schema[0]['AttributeName']
        return pkey
    except Exception as e:
        detail = f'Error getting table keys from DynamoDB: {str(e)}'
        handle_error(e,detail)


def get_params_from_item(key:str, table_name:str, params:list):
    '''This function retrieves specific parameters from a DynamoDB table item.
    
    Parameters:
        key : str
            The key of the item that will be retrieved from the DynamoDB table.
        table_name : str
            The name of the DynamoDB table where the item is stored.
        params : list
            A list of strings representing the names of the attributes that will be retrieved from the DynamoDB item.

    Return:
        dict
    '''
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        key_pair = {get_table_keys(table_name): key}

        response = table.get_item(Key=key_pair)
        item = response['Item']
        return {param: item[param] for param in params}
    except Exception as e:
        detail = f'Error getting params from DynamoDB: {str(e)}'
        handle_error(e,detail)


def update_item(key:str, table_name:str, update_dict:dict):
    """This function update data from an specific item on a DynamoDB table.
    
    Parameters:
        key : str
            The key of the item that will be updated in the DynamoDB table.
        table_name : str
            The name of the DynamoDB table where the item is stored.
        update_dict : dict
            A dictionary where each key-value pair represents an attribute name and its new value that will be updated in the DynamoDB item.
        
    Return:
        None
    """
    dynamodb = boto3.resource('dynamodb')
    dynamodb = dynamodb.Table(table_name)
    key_pair = {get_table_keys(table_name): key}

    for param, value in update_dict.items():
        dynamodb.update_item(
            Key=key_pair,
            UpdateExpression=f'SET {param} = :val',
            ExpressionAttributeValues={':val': value}
        )

    print(f'DynamoDB updated successfully - {dt.datetime.now()}')