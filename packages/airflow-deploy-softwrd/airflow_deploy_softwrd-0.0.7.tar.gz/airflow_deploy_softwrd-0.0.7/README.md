# Airflow Deploy Softwrd

A Flask application to handle POSTMAN webhooks for deploying and taking down repositories using Docker Compose. This application is particularly designed for managing Airflow deployment of softwrd in house hosted repositories.

## Features
- Deploy specified branches of a repository on push events.
- Bring down specified branches of a repository.
- Retrieve secrets from AWS Secrets Manager.
- Automatically configure environment variables from secrets.

## Prerequisites
- Python 3.9 or higher
- Docker and Docker Compose
- AWS credentials setup if using Secrets Manager

## Installation

You can install the package from PyPI:

```bash
pip install airflow_deploy_softwrd
```

## Configuration

### AWS Credentials Setup
Set up your AWS credentials using the following command:
```bash
$Env:AWS_ACCESS_KEY_ID = "your-access-key-id"
$Env:AWS_SECRET_ACCESS_KEY = "your-secret-access-key"
```
you must have to set up your AWS credentials in your environment variables before running the application.

## Usage

To run the server, use the following command:

```bash
airflow_deploy_softwrd /path/to/your/working/directory /path/to/config.json
```

### Command Line Arguments
- `/path/to/your/working/directory`: The base directory where repositories will be cloned and operated.
- `/path/to/config.json`: Path to the configuration file containing allowed branches.

### Configuration File
Create a JSON configuration file, e.g., `config.json`, with the following contents to specify allowed branches:

```json
{
  "allowed_branches": ["develop", "main", "Airflow-Changelog"]
}
```




### Secrets in AWS Secrets Manager
Set up the following secrets in AWS Secrets Manager:
- `airflow_deployment_env`: Secret containing environment variables for deploying Airflow.
- `airflow_variables_env`: Secret containing Airflow variable configurations.

### POSTMAN Webhooks
Set up POSTMAN webhooks to point to the following endpoints of your running Flask application:

- Deploying a branch: 
  ```
  http://localhost:6969/payload
  ```

- Bringing down a branch: 
  ```
  http://localhost:6969/putdown
  ```

## Example Webhook Payloads

### Deploy a Branch
The webhook for deploying a branch should contain information about the branch and repository in the body of the payload:

```json
{
  "ref": "refs/heads/main",
  "repository": {
    "clone_url": "https://github.com/yourusername/yourrepo.git",
    "name": "yourrepo"
  },
  "head_commit": {
    "message": "Your commit message"
  }
}
```

### Bring Down a Branch
The webhook for bringing down a branch should contain similar information:

```json
{
  "ref": "refs/heads/main",
  "repository": {
    "clone_url": "https://github.com/yourusername/yourrepo.git",
    "name": "yourrepo"
  },
  "head_commit": {
    "message": "Your commit message"
  }
}
```

## Contact

Maintainer: [Md Robiuddin](mailto:robiuddin@softwrd.ai)

Project Link: [Repository URL](https://github.com/softwrdai/airflow_deploy_softwrd/)