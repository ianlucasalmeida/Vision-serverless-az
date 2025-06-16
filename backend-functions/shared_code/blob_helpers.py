import os
from azure.storage.blob import BlobServiceClient

# Pega a string de conexão das configurações da Function App
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

def upload_to_blob(container_name: str, blob_name: str, data: bytes, return_url: bool = False):
    """
    Faz o upload de dados para um contêiner no Azure Blob Storage.
    """
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(data, overwrite=True)
    
    if return_url:
        return blob_client.url
    return True