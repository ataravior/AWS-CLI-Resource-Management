import boto3
from tabulate import tabulate
from utils.utils import user_input

route53 = boto3.client("route53")

def create_dns_record():
    zone_id = input("Enter the Hosted Zone ID: ").strip()
    record_name = input("Enter the record name (e.g., www.example.com): ").strip()
    record_type = user_input("Select record type:", ["A", "CNAME"])
    record_value = input("Enter the record value (IP for A, domain for CNAME): ").strip()

    response = route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Changes": [
                {
                    "Action": "CREATE",
                    "ResourceRecordSet": {
                        "Name": record_name,
                        "Type": record_type,
                        "TTL": 300,
                        "ResourceRecords": [{"Value": record_value}]
                    }
                }
            ]
        }
    )

    print(f"DNS Record '{record_name}' ({record_type}) created successfully!")

def list_dns_records():
    zone_id = input("Enter the Hosted Zone ID: ").strip()

    response = route53.list_resource_record_sets(HostedZoneId=zone_id)
    records = [[r["Name"], r["Type"], ", ".join([v["Value"] for v in r.get("ResourceRecords", [])])]
               for r in response["ResourceRecordSets"]]

    print("\n**List of DNS Records**")
    print(tabulate(records, headers=["Name", "Type", "Value"], tablefmt="grid"))

def delete_dns_record():
    zone_id = input("Enter the Hosted Zone ID: ").strip()
    record_name = input("Enter the record name to delete: ").strip()
    record_type = user_input("Select record type:", ["A", "CNAME"])

    confirm = input(f"Are you sure you want to delete '{record_name}' ({record_type})? (YES/NO): ").strip().upper()
    if confirm == "YES":
        route53.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                "Changes": [
                    {
                        "Action": "DELETE",
                        "ResourceRecordSet": {
                            "Name": record_name,
                            "Type": record_type,
                            "TTL": 300,
                            "ResourceRecords": [{"Value": "DELETE"}]  
                        }
                    }
                ]
            }
        )
        print(f"DNS Record '{record_name}' deleted successfully!")
