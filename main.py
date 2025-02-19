from services import aws_ec2
from services import aws_s3
from services import aws_route53
from services.aws_route53_records import list_dns_records
from services.aws_route53_zones import list_hosted_zones
from utils.utils import user_input

while True:
    sector_choice = user_input("Select a sector:", ["EC2 Instances", "S3 Buckets", "Route53", "Exit"])
    
    if sector_choice == "Exit":
        print("Exiting setup...")
        break

    if sector_choice == "EC2 Instances":
        aws_ec2.manage_ec2()

    elif sector_choice == "S3 Buckets":
        aws_s3.manage_s3()

    elif sector_choice == "Route53":
        aws_route53.manage_route53()  
