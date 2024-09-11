import argparse
import os
import subprocess
import signal
import boto3
import datetime
from botocore.exceptions import NoCredentialsError, ClientError

def usage():
    print("Usage: anchorestig static <IMAGE> [-u registry_username] [-p registry_password] [-r registry_url] [-l] [-s] [-a AWS S3 Bucket name] [-c Anchore STIG UI Account]")
    exit(1)

def upload_to_s3(bucket_name, file, origin_dir, account, image_digest, image_name, date_prefix):
    """
    Upload files from a specified directory to an AWS S3 bucket.

    :param bucket_name: Name of the S3 bucket.
    :param directory: Directory containing files to upload.
    """

    if "@" in image_name:
        image_name = image_name.split('@')[0] + ':' + "NOTAG"
    
    if "." not in image_name.split(':')[0]:
        image_name = "docker.io/" + image_name
    tag = image_name.split(':')[-1]
    registry = image_name.split('/', 1)[0]
    repository = image_name.split('/', 1)[-1].split(":")[0].replace("/", "-")
    date_filename = add_date_prefix(file, date_prefix)
    # Initialize S3 client with custom credentials
    s3 = boto3.client('s3')

    try:
        # Walk through the directory and upload files
        file_path = f"anchore/{account}/{registry}/{repository}/{tag}/{image_digest}/{date_filename}"
        s3.upload_file(f"{origin_dir}/{file}", bucket_name, file_path)
        print(f"Uploaded '{file}@{image_digest}' to '{bucket_name}' bucket.")
    except NoCredentialsError:
        print("Error: AWS credentials not found.")
    except ClientError as e:
        print(f"Error: {e}")

def get_image_digest(image, username, password, url, insecure, local_image):
    if local_image:
        result = subprocess.run(["docker", "inspect", '--format="{{index .Id}}"', image], capture_output = True, text = True)
        return result.stdout.replace('"', '').replace('\n', '')
    elif not username:
        subprocess.run(["docker", "pull", image])
        result = subprocess.run(["docker", "inspect", '--format="{{index .Id}}"', image], capture_output = True, text = True)
        subprocess.run(["docker", "rmi", image])
        return result.stdout.replace('"', '').replace('\n', '')
    else:
        subprocess.run(["docker", "--config", "./stig-docker-config", "login", url, "-u", username, "-p", password])
        subprocess.run(["docker", "pull", image])
        result = subprocess.run(["docker", "inspect", '--format="{{index .Id}}"', image], capture_output = True, text = True)
        subprocess.run(["docker", "rmi", image])
        return result.stdout.replace('"', '').replace('\n', '')

def add_date_prefix(filename, date_prefix):
    split_filename = filename.rsplit(".", 1)
    return split_filename[0] + date_prefix + "." + split_filename[-1]


def static_analysis(username, password, url, insecure, local_image, image, aws_s3_bucket_upload, account):

    if not image:
        usage()

    dir_name = image.replace("/", "-").replace(":", "-")
    os.makedirs(f"stig-results/{dir_name}", exist_ok=True)

    sanitized_image_name = dir_name

    subprocess.run(["docker", "volume", "create", "stig-runner"])

    def cleanup_volume(signum, frame):
        subprocess.run(["docker", "volume", "rm", "stig-runner"])
        exit(1)

    signal.signal(signal.SIGINT, cleanup_volume)

    if local_image:
        print("Detected local image. Running in local mode.")
        subprocess.run(["docker", "save", image, "-o", "./local-image.tar.gz"])
        subprocess.run(["docker", "run", "-t", "--rm", "--privileged",
                        "-e", f"SCAN_IMAGE={image}",
                        "-e", f"INSECURE_REG={insecure}",
                        "--name", "stig-runner",
                        "-v", f"{os.getcwd()}/local-image.tar.gz:/etc/local-image.tar.gz:ro",
                        "-v", f"{os.getcwd()}/stig-results/{dir_name}:/tmp",
                        "anchore/static-stig:latest"])
        os.remove("local-image.tar.gz")
    elif not username:
        subprocess.run(["docker", "run", "-t", "--rm", "--privileged",
                        "-e", f"SCAN_IMAGE={image}",
                        "-e", f"INSECURE_REG={insecure}",
                        "--name", "stig-runner",
                        "-v", f"{os.getcwd()}/stig-results/{dir_name}:/tmp",
                        "anchore/static-stig:latest"])
    else:
        subprocess.run(["docker", "run", "-t", "--rm", "--privileged",
                        "-e", f"SCAN_IMAGE={image}",
                        "-e", f"INSECURE_REG={insecure}",
                        "-e", f"REGISTRY_USERNAME={username}",
                        "-e", f"REGISTRY_PASSWORD={password}",
                        "-e", f"REGISTRY_URL={url}",
                        "--name", "stig-runner",
                        "-v", f"{os.getcwd()}/stig-results/{dir_name}:/tmp",
                        "anchore/static-stig:latest"])

    if aws_s3_bucket_upload:
        image_digest = get_image_digest(image, username, password, url, insecure, local_image)
        date_prefix = str(datetime.datetime.now().timestamp()).replace(" ", "_").split(".")[0]
        for file in os.listdir(f"{os.getcwd()}/stig-results/{dir_name}"):
            upload_to_s3(aws_s3_bucket_upload, file, f"{os.getcwd()}/stig-results/{dir_name}", account, image_digest, image, date_prefix)
