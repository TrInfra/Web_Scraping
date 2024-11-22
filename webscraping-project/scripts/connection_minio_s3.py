import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError

def connection_minio():
    """
    Estabelece conexão com o serviço MinIO.
    """
    load_dotenv()
    s3 = boto3.client(
        's3',
        endpoint_url=os.getenv('MINIO_URL'),  # URL sem a porta
        aws_access_key_id=os.getenv('MINIO_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('MINIO_SECRET_ACCESS_KEY'),
        verify=False  # Ignora a verificação do SSL para testes
    )
    return s3

def check_connection(s3):

    """

    Verifica se a conexão com o MinIO está ativa.

    """

    try:

        s3.list_buckets()  # Tenta listar os buckets

        return True

    except (NoCredentialsError, ClientError) as e:

        print(f"Erro ao conectar: {e}")

        return False

def upload_file(s3, file_name, bucket, object_name=None):

    """

    Envia um arquivo para um bucket no MinIO.

    """

    if object_name is None:

        object_name = file_name


    try:

        s3.upload_file(file_name, bucket, object_name)

        print(f"Arquivo {file_name} enviado para o bucket {bucket} com sucesso.")

    except ClientError as e:

        print(f"Erro ao enviar arquivo: {e}")

s3 = connection_minio()
check_connection(s3)
upload_file(s3, r"C:\Users\srdes\OneDrive\Área de Trabalho\projetos\Web_Scraping\webscraping-project\data\CSVs_Files\monitor.csv", "teste-nyck")