import sys
import json
import os
import subprocess
import threading
import time
import datetime

import boto3
from botocore.exceptions import ClientError
from flask import Flask, request

app = Flask(__name__)
repo_base_path = None
allowed_branches = []

def initialize_app(base_path, config_path):
    global repo_base_path, allowed_branches
    repo_base_path = base_path

    # Load allowed branches from config file
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        allowed_branches = config.get("allowed_branches", [])

def get_secret(secret_name):
    """
    Retrieve secret value from AWS Secrets Manager.
    
    Args:
        secret_name (str): Name of the secret in AWS Secrets Manager.

    Returns:
        dict: Secret value in JSON format.
    
    Raises:
        ClientError: If there is an error retrieving the secret value.
    """
    region_name = "eu-north-1"
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    secret = get_secret_value_response["SecretString"]
    return json.loads(secret)

def down_the_repo(branch, repo_name, clone_url):
    if branch in allowed_branches:
        if os.path.isdir(repo_name):
            print("Directory exists")
            os.chdir(f"{repo_base_path}/{repo_name}")
            subprocess.run(["git", "checkout", branch])
            subprocess.run(["docker-compose", "down"])
            os.chdir(repo_base_path)
            os.remove(f"{repo_base_path}/{repo_name}")
        else:
            print("Directory does not exist")

def deploy_the_repo(branch, repo_name, clone_url):
    if branch in allowed_branches:
        if os.path.isdir(repo_name):
            print("Directory exists")
            os.chdir(f"{repo_base_path}/{repo_name}")
            subprocess.run(["git", "pull", "origin", branch])
            subprocess.run(["git", "checkout", branch])
        else:
            print("Directory does not exist")
            subprocess.run(["git", "clone", "--branch", branch, clone_url, f"{repo_base_path}/{repo_name}"])
            os.chdir(f"{repo_base_path}/{repo_name}")
            subprocess.run(["git", "checkout", branch])
        
        envs = get_secret("airflow_deployment_env")
        if envs:
            print("Setting environment variables")
            for key in envs.keys():
                os.environ[key] = envs[key]

            os.environ["CACHEBUST"] = str((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())

            vars = get_secret("airflow_variables_env")
            if vars:
                print("Setting Airflow variables")
                with open(f"{repo_base_path}/{repo_name}/airflow/vars.json", "w") as f:
                    json.dump(vars, f)
            else:
                print("Airflow variables not found")
                with open(f"{repo_base_path}/{repo_name}/airflow/vars.json", "w") as f:
                    json.dump({}, f)

            subprocess.run(["docker-compose", "down"])
            time.sleep(2)
            subprocess.run(["docker-compose", "up", "-d", "--build"])
        else:
            print("Environment variables not found")

@app.route("/putdown", methods=["POST"])
def github_putdown():
    json_data = request.json

    try:
        branch = json_data["ref"].split("/")[-1]
        clone_url = json_data["repository"]["clone_url"]
        commit_message = json_data["head_commit"]["message"]
        repo_name = json_data["repository"]["name"]
    except:
        return "Skipped!", 200

    if branch not in allowed_branches:
        return "Branch not allowed!", 403

    print("Branch:", branch)
    print("Clone URL:", clone_url)
    print("Commit Message:", commit_message)
    os.chdir(repo_base_path)

    threading.Thread(target=down_the_repo, args=(branch, repo_name, clone_url)).start()

    return "Down Request Accepted", 202

@app.route("/payload", methods=["POST"])
def github_payload():
    json_data = request.json

    try:
        branch = json_data["ref"].split("/")[-1]
        clone_url = json_data["repository"]["clone_url"]
        commit_message = json_data["head_commit"]["message"]
        repo_name = json_data["repository"]["name"]
    except:
        return "Skipped!", 200

    if branch not in allowed_branches:
        return "Branch not allowed!", 403

    print("Branch:", branch)
    print("Clone URL:", clone_url)
    print("Commit Message:", commit_message)
    os.chdir(repo_base_path)

    threading.Thread(target=deploy_the_repo, args=(branch, repo_name, clone_url)).start()
    
    return "Accepted!", 202

def main():
    if len(sys.argv) != 3:
        print("Usage: airflow_deploy_softwrd <path> <config_path>")
        sys.exit(1)

    initialize_app(sys.argv[1], sys.argv[2])
    app.run(host="0.0.0.0", port=6969)

if __name__ == "__main__":
    main()