import boto3
from tabulate import tabulate
route53 = boto3.client("route53")

def create_hosted_zone():
    domain_name = input("Enter the domain name for the hosted zone: ").strip()

    response = route53.create_hosted_zone(
        Name=domain_name,
        CallerReference=domain_name,
        HostedZoneConfig={"Comment": "Created via CLI", "PrivateZone": False}
    )

    hosted_zone_id = response["HostedZone"]["Id"].split("/")[-1]

    route53.change_tags_for_resource(
        ResourceType="hostedzone",
        ResourceId=hosted_zone_id,
        AddTags=[
            {"Key": "CreatedBy", "Value": "CLI"},
            {"Key": "Owner", "Value": "avioratar"}
        ]
    )

    print(f"Hosted Zone '{domain_name}' created successfully! Zone ID: {hosted_zone_id}")

def list_hosted_zones():
    response = route53.list_hosted_zones()
    zones = []

    for zone in response["HostedZones"]:
        tags = route53.list_tags_for_resource(ResourceType="hostedzone", ResourceId=zone["Id"].split("/")[-1])
        tag_dict = {tag["Key"]: tag["Value"] for tag in tags["ResourceTagSet"]["Tags"]}

        if tag_dict.get("CreatedBy") == "CLI":
            zones.append([zone["Id"].split("/")[-1], zone["Name"], tag_dict.get("Owner", "N/A")])

    if zones:
        print("\n**List of Hosted Zones (Created via CLI)**")
        print(tabulate(zones, headers=["Zone ID", "Domain", "Owner"], tablefmt="grid"))
    else:
        print("No Hosted Zones found.")

def delete_hosted_zone():
    zone_id = input("Enter the Hosted Zone ID to delete: ").strip()

    confirm = input(f"Are you sure you want to delete Hosted Zone '{zone_id}'? (YES/NO): ").strip().upper()
    if confirm == "YES":
        route53.delete_hosted_zone(Id=zone_id)
        print(f"Hosted Zone '{zone_id}' deleted successfully!")
