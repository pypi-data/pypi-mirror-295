from datasets import Dataset
import requests
import os
import tempfile
import uuid


def get_presigned_url(file_name: str, bucket_name: str = "creaodev"):
    url = "https://drk3mkqa6b.execute-api.us-west-2.amazonaws.com/default/minimaxserver"
    api_key = os.environ["CREAO_API_KEY"]
    headers = {"Content-Type": "application/json", "x-api-key": api_key}
    # Payload to be sent to the Lambda function via API Gateway
    payload = {"action": "s3", "file_name": file_name, "bucket_name": bucket_name}
    # Send the request
    response = requests.post(url, headers=headers, json=payload)
    print("reponse:", response.json())
    return response.json()["url"]


def submit_pipeline_job(
    pipeline_name: str, pipe_yaml: str, run_config_template: str, dataset: Dataset
):
    """
    Submit a pipeline job to the Creao server
    :param pipeline_name: The name of the pipeline
    :param pipe_yaml: The pipeline YAML
    :param run_config_template: The run configuration template
    :param dataset: The dataset to use
    :return: The response from the server
    """
    pipeline_id = str(uuid.uuid4())
    pipe_yaml = pipe_yaml.replace("pipeline_id_default", pipeline_id)
    # generate a random file name for the dataset based on uuid
    file_name = str(uuid.uuid4()) + ".parquet"
    bucket_name = "creaodev"
    temp_file_path = f"/tmp/{file_name}"
    # save the dataset to a temporary file
    # Use tempfile to create a temporary file
    # Save the dataset as a Parquet file
    dataset.to_parquet(temp_file_path)
    print(f"Dataset saved to temporary file: {temp_file_path}")

    # get the presigned url for the dataset
    presigned_url = get_presigned_url(file_name, bucket_name)

    # Open the zip file and upload it using the pre-signed URL
    with open(temp_file_path, "rb") as f:
        upload_response = requests.put(presigned_url, data=f)

    # Check the response from the upload
    if upload_response.status_code == 200:
        print("File uploaded successfully")
    else:
        print(
            "Upload failed with status code:",
            upload_response.status_code,
            upload_response.text,
        )
    print("final clean up")
    # (Optional) Clean up the temporary file when done
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
        print(f"Temporary file {temp_file_path} has been removed.")

    # generate a uuid
    s3_path = f"s3://{bucket_name}/{file_name}"
    api_key = os.environ["CREAO_API_KEY"]
    payload = {
        "pipeline_id": pipeline_id,
        "pipeline_name": pipeline_name,
        "pipe_yaml": pipe_yaml,
        "run_config_template": run_config_template,
        "dataset_s3_path": s3_path,
        "api_key": api_key,
        "action": "pipeline",
    }
    # The API Gateway endpoint URL
    url = "https://drk3mkqa6b.execute-api.us-west-2.amazonaws.com/default/minimaxserver"
    headers = {"Content-Type": "application/json", "x-api-key": api_key}
    # Payload to be sent to the Lambda function via API Gateway
    # Send the request
    response = requests.post(url, headers=headers, json=payload)
    # print("reponse:", response.content)
    try:
        return response.json()
    except Exception as e:
        print(f"create pipeline failed with error:{e}, with response:{response.text}")
