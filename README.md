# Cloudflare R2 Migration Tool

## Overview

This tool facilitates a "Sippy-based" migration from AWS S3 to Cloudflare R2. Instead of migrating all your data at once, Sippy fetches data from your AWS S3 bucket and moves it to Cloudflare R2 only when it's accessed. This ensures a seamless transition with minimal downtime. The tool also assists in updating Python code references from AWS S3 to Cloudflare R2.

## Prerequisites

### 1. Cloudflare Account

- If you don't have a Cloudflare account, sign up at [Cloudflare Registration](https://dash.cloudflare.com/sign-up).
- After signing up, note down your `account_id` from the Cloudflare dashboard.

### 2. Install and Set Up Wrangler

- Install Wrangler globally using `npm` (Node.js package manager):

npm install -g @cloudflare/wrangler

csharp


- Authenticate Wrangler with your Cloudflare account:

```
wrangler login
```

This will open a Cloudflare login page in your web browser. Sign in to grant Wrangler access.

### 3. AWS Credentials

- You should have an AWS account with an S3 bucket that you want to migrate.
- Note down your AWS `access_key_id` and `secret_access_key` with appropriate permissions. These are required for Sippy to migrate data.

### 4. Cloudflare R2 Credentials

- In the Cloudflare dashboard, navigate to the R2 section.
- Generate or note down your R2 `access_key_id` and `secret_access_key`.

### 5. Python Environment

- Ensure Python 3.x is installed.
- It's recommended to create a virtual environment for isolating the dependencies.
- You might need additional libraries like `requests`. Install them using pip:

```
pip install requests
```


## Usage

### 1. Clone the Repository

```
git clone <repository-url>
cd <repository-directory>
```


### 2. Run the Script

The script will prompt you for various credentials and other necessary information. 

```
python migration_script.py
```


### 3. Follow the Prompts

- The script will ask you for various inputs like Cloudflare account ID, API token, AWS credentials, and the directory path for the Python codebase.
- If you already have a Cloudflare R2 bucket created, you can skip the bucket creation step and provide the existing bucket name when prompted.
- The script will also ask for the AWS region. If not provided, it will default to 'auto'.

### 4. Verify the Migration

- After the script runs successfully, verify that your data has been migrated to the specified R2 bucket.
- Check the Python codebase to ensure AWS S3 references are updated to Cloudflare R2.

## Troubleshooting

- If you encounter issues with Wrangler, refer to the [official Wrangler documentation](https://developers.cloudflare.com/wrangler/).
- For issues related to the Cloudflare R2 API, consult the [R2 documentation](https://developers.cloudflare.com/r2/).