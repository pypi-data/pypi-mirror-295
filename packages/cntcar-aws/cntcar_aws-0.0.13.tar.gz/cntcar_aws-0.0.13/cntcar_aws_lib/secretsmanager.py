import boto3
import json
from .utils import handle_error

def get_secret(secret_name:str, key_name:str=None):
    """This function retrieves a secret value from AWS Secrets Manager.

    Parameters:
        secret_name : str
            The name or ARN of the secret to retrieve.
        key_name : str
            The key name of the secret value to retrieve. If None, the entire secret will be returned.

    Return:
        Specific secret value (str) or the entire secret (dict).
    """
    try:
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager')
        
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])

        if key_name:
            value = secret.get(key_name)

            if value:
                print(f'Secret retrieved successfully: {secret_name} - {key_name}')
                return value
            else:
                print(f'key {key_name} not found in secret {secret_name}')
                return None
        
        else:
            print(f'Secret retrieved successfully: {secret_name}')
            return secret
            
    except Exception as e:
        detail = f'Error retrieving secret: {secret_name} - {key_name}'
        handle_error(e,detail)