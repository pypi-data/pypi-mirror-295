import requests
import zipfile
from io import BytesIO
import os

SAMPLES_API_ENDPOINT = "https://z8vxfzxgdg.execute-api.eu-west-2.amazonaws.com/samples"

def load_dataset_samples(org_id: str, dataset_name: str, save_path: str = 'downloads'):
    """Retrieve and download sample data for a dataset."""
    try:
        print(f"Fetching samples...")
        
        # Construct the API request
        params = {
            "orgId": org_id,
            "datasetName": dataset_name
        }
        
        # Fetch the presigned URL for samples
        response = requests.get(SAMPLES_API_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        presigned_url = data['presigned_url']
        
        # Download the zip file
        response = requests.get(presigned_url)
        response.raise_for_status()
        
        # Extract the contents
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            for file_info in zip_ref.infolist():
                if not file_info.filename.startswith('__MACOSX'):
                    zip_ref.extract(file_info, save_path)
        
        # Remove any empty directories
        for root, dirs, files in os.walk(save_path, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
        
        print(f"Sample data downloaded and extracted successfully to {save_path}.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sample data: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
