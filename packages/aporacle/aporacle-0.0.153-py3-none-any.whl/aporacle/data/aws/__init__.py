import csv

import boto3
import pandas as pd
from io import StringIO
from io import BytesIO
import json
from botocore.exceptions import NoCredentialsError, ClientError


def upload_data_to_aws(data, bucket, s3_file):
    # Convert the list to a DataFrame
    df = pd.DataFrame(data)

    # Use StringIO to save DataFrame to a CSV in memory
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, header=False)

    # Get the CSV string from the buffer
    csv_content = csv_buffer.getvalue()

    # Initialize S3 client
    s3 = boto3.client('s3')

    try:
        # Upload CSV to S3
        s3.put_object(Bucket=bucket, Key=s3_file, Body=csv_content)
        return True
    except NoCredentialsError as nce:
        raise nce
    except Exception as e:
        raise e


def upload_file_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3')

    try:
        s3.upload_file(local_file, bucket, s3_file)
        return True
    except FileNotFoundError as fnfe:
        raise fnfe
    except NoCredentialsError as nce:
        raise nce


def download_file_from_aws(bucket, s3_file, local_file):
    s3 = boto3.client('s3')

    try:
        s3.download_file(bucket, s3_file, local_file)
        return True
    except FileNotFoundError as fnfe:
        raise fnfe
    except NoCredentialsError as nce:
        raise nce
    except Exception as e:
        raise e


def download_json_from_s3_to_dict(bucket, s3_file):
    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Create a BytesIO object to hold the file content in memory
    file_content = BytesIO()

    try:
        # Download the file from S3 into the BytesIO object
        s3.download_fileobj(bucket, s3_file, file_content)

        # Move the cursor to the beginning of the BytesIO object
        file_content.seek(0)

        # Read the JSON file content into a dictionary
        data = json.load(file_content)

        # print(f"Download and conversion successful: {bucket}/{s3_file}")
        return data
    except NoCredentialsError as nce:
        raise nce
    except Exception as e:
        raise e


def download_csv_from_s3_to_dataframe(bucket, s3_file, header=True):
    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Create a BytesIO object to hold the file content in memory
    file_content = BytesIO()

    try:
        # Download the file from S3 into the BytesIO object
        s3.download_fileobj(bucket, s3_file, file_content)

        # Move the cursor to the beginning of the BytesIO object
        file_content.seek(0)

        # Read the CSV file content into a Pandas DataFrame
        df = pd.read_csv(file_content, header=header)

        # print(f"Download and conversion successful: {bucket}/{s3_file}")
        return df

    except NoCredentialsError as nce:
        raise nce
    except ClientError as ce:
        raise ce
    except Exception as e:
        raise e


def download_csv_from_s3_to_list(bucket, s3_file):
    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Create a BytesIO object to hold the file content in memory
    file_content = BytesIO()

    try:
        # Download the file from S3 into the BytesIO object
        s3.download_fileobj(bucket, s3_file, file_content)

        # Move the cursor to the beginning of the BytesIO object
        file_content.seek(0)

        # Read the CSV file content into a list of rows
        csv_content = StringIO(file_content.getvalue().decode('utf-8'))
        csv_reader = csv.reader(csv_content)
        rows = list(csv_reader)

        print(f"Download and conversion successful: {bucket}/{s3_file}")
        return rows
    except NoCredentialsError as nce:
        raise nce
    except ClientError as ce:
        raise ce
    except Exception as e:
        raise e
