import boto3
from tabulate import tabulate
from utils.utils import user_input

s3 = boto3.client("s3")

def list_s3_buckets():
    """List only S3 buckets that belong to the user (created by Pulumi or with a specific tag)"""
    response = s3.list_buckets()
    buckets = []

    for bucket in response["Buckets"]:
        bucket_name = bucket["Name"]
        
        try:
            tags_response = s3.get_bucket_tagging(Bucket=bucket_name)
            tags = {tag["Key"]: tag["Value"] for tag in tags_response["TagSet"]}
            
            if tags.get("CreatedBy") == "Pulumi" or "Owner" in tags:
                buckets.append([bucket_name, tags.get("Owner", "N/A")])
        except s3.exceptions.ClientError:
            pass

    if buckets:
        print("\n **List of Your S3 Buckets**")
        print(tabulate(buckets, headers=["Bucket Name", "Owner"], tablefmt="grid"))
    else:
        print("\n No S3 buckets found.")

def upload_file_to_s3():
    bucket_name = input("Enter the name of the S3 bucket: ").strip()
    file_path = input("Enter the file path to upload: ").strip()

    try:
        s3.upload_file(file_path, bucket_name, file_path.split("/")[-1])
        print(f" File uploaded to '{bucket_name}'.")
    except Exception as e:
        print(f" Error uploading file: {e}")

def delete_s3_bucket():
    bucket_name = input("Enter the name of the S3 bucket to delete: ").strip()
    confirm = input(f" Are you sure you want to delete '{bucket_name}'? (YES/NO): ").strip().upper()
    if confirm == "YES":
        try:
            s3.delete_bucket(Bucket=bucket_name)
            print(f" S3 bucket '{bucket_name}' deleted successfully.")
        except Exception as e:
            print(f" Error deleting bucket: {e}")

def create_s3_bucket():
    bucket_name = input("Enter a name for the new S3 bucket: ").strip()
    bucket_type = user_input("Public or Private?", ["Public", "Private"])

    if bucket_type == "Public":
        confirm = input(f"Are you sure you want to create a PUBLIC bucket '{bucket_name}'? (YES/NO): ").strip().upper()
        if confirm != "YES":
            return
    try:
        s3.create_bucket(Bucket=bucket_name)
        
        s3.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={"TagSet": [{"Key": "Owner", "Value": "avioratar"}, {"Key": "CreatedBy", "Value": "Pulumi"}]}
        )

        print(f"S3 bucket '{bucket_name}' created successfully.")
    except Exception as e:
        print(f" Error creating bucket: {e}")

def manage_s3():
    while True:
        s3_action = user_input("Select an action:", ["Manage S3 Bucket", "Create S3", "Exit"])
        if s3_action == "Exit":
            break
        elif s3_action == "Manage S3 Bucket":
            while True:
                manage_s3_action = user_input("Select action:", ["List Buckets", "File Upload", "Delete S3", "Exit"])
                if manage_s3_action == "Exit":
                    break
                elif manage_s3_action == "List Buckets":
                    list_s3_buckets()
                elif manage_s3_action == "File Upload":
                    upload_file_to_s3()
                elif manage_s3_action == "Delete S3":
                    delete_s3_bucket()
        elif s3_action == "Create S3":
            create_s3_bucket()
