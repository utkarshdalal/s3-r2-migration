import os
import requests
import re

CLOUDFLARE_API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts"

def create_bucket(account_id, api_token, bucket_name):
    url = f"{CLOUDFLARE_API_BASE_URL}/{account_id}/r2/buckets"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = {
        "name": bucket_name
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def enable_sippy(account_id, api_token, bucket_name, aws_access_key, aws_secret_key, r2_access_key, r2_secret_key):
    url = f"{CLOUDFLARE_API_BASE_URL}/{account_id}/r2/buckets/{bucket_name}/sippy"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    data = {
        "provider": "AWS",
        "bucket": bucket_name,
        "key_id": aws_access_key,
        "access_key": aws_secret_key,
        "r2_key_id": r2_access_key,
        "r2_access_key": r2_secret_key
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

def update_codebase(directory, account_id, region='auto'):
    r2_endpoint = f'https://{account_id}.r2.cloudflarestorage.com'
    
    # Replacement template for both resource and client initializations for R2
    replacement_template = f'boto3.{{}}("s3", region_name="{region}", endpoint_url="{r2_endpoint}", aws_access_key_id=os.environ["R2_ACCESS_KEY"], aws_secret_access_key=os.environ["R2_SECRET_KEY"])'
    
    # Patterns to match various boto3 initializations for 's3'
    patterns = [
        r'boto3\.resource\(\s*?[\'"]s3[\'"].*?\)',
        r'boto3\.client\(\s*?[\'"]s3[\'"].*?\)'
    ]

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    for pattern in patterns:
                        if 'resource' in pattern:
                            content = re.sub(pattern, replacement_template.format('resource'), content)
                        else:
                            content = re.sub(pattern, replacement_template.format('client'), content)
                
                with open(file_path, 'w') as f:
                    f.write(content)
                print(f"Updated file: {file_path}")

if __name__ == "__main__":
    # Prompt for sensitive data and set as environment variables
    os.environ["CLOUDFLARE_ACCOUNT_ID"] = input("Enter your Cloudflare account ID: ")
    os.environ["CLOUDFLARE_API_TOKEN"] = input("Enter your Cloudflare API token: ")
    os.environ["AWS_ACCESS_KEY"] = input("Enter AWS Access Key ID: ")
    os.environ["AWS_SECRET_KEY"] = input("Enter AWS Secret Access Key: ")
    os.environ["R2_ACCESS_KEY"] = input("Enter R2 Access Key ID: ")
    os.environ["R2_SECRET_KEY"] = input("Enter R2 Secret Access Key: ")

    # Decide to create a bucket or not
    create_bucket_choice = input("Do you want to create a new Cloudflare R2 bucket? (yes/no): ")
    if create_bucket_choice.lower() == "yes":
        os.environ["BUCKET_NAME"] = input("Enter the Cloudflare R2 bucket name: ")
        create_bucket_response = create_bucket(os.environ["CLOUDFLARE_ACCOUNT_ID"], os.environ["CLOUDFLARE_API_TOKEN"], os.environ["BUCKET_NAME"])
        print(create_bucket_response)
    else:
        os.environ["BUCKET_NAME"] = input("Enter the name of the existing Cloudflare R2 bucket: ")

    # Take region input from the user or set to 'auto'
    region = input("Enter the Cloudflare bucket region (leave blank for 'auto'): ")
    if not region:
        region = 'auto'

    # Enabling Sippy and Updating the codebase
    sippy_response = enable_sippy(os.environ["CLOUDFLARE_ACCOUNT_ID"], os.environ["CLOUDFLARE_API_TOKEN"], os.environ["BUCKET_NAME"], os.environ["AWS_ACCESS_KEY"], os.environ["AWS_SECRET_KEY"], os.environ["R2_ACCESS_KEY"], os.environ["R2_SECRET_KEY"])
    print(sippy_response)

    directory = input("Enter the directory path of your Python codebase: ")
    update_codebase(directory, os.environ["CLOUDFLARE_ACCOUNT_ID"], region)